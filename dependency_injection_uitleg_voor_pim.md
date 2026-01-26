# Dependency Injection Uitleg voor Pim

Dit document legt uit wat we hebben veranderd in de codebase en waarom. We zijn overgestapt van `@staticmethod` naar **Dependency Injection** (DI) met FastAPI.

---

## Inhoudsopgave

1. [Het Probleem: Wat was er mis?](#het-probleem-wat-was-er-mis)
2. [Wat is een Static Method?](#wat-is-een-static-method)
3. [Wat is een Class Method?](#wat-is-een-class-method)
4. [Wat is Dependency Injection?](#wat-is-dependency-injection)
5. [Hoe werkt Depends() in FastAPI?](#hoe-werkt-depends-in-fastapi)
6. [De Wijzigingen die we hebben gemaakt](#de-wijzigingen-die-we-hebben-gemaakt)
7. [Vergelijking met Spring Boot](#vergelijking-met-spring-boot)
8. [Voordelen van Dependency Injection](#voordelen-van-dependency-injection)

---

## Het Probleem: Wat was er mis?

De oude code gebruikte `@staticmethod` overal, maar dat werkte niet correct:

```python
# OUD - BROKEN CODE
class GameSystemService:
    @staticmethod
    def add_system(api_system: APIGameSystem) -> APIGameSystemResponse:
        system = GameSystemMapper.api_system_to_system(api_system)
        GameSystemRepository.add_new_system(system)  # ❌ Dit werkt niet!
        return GameSystemMapper.game_system_to_api_game_system_response(system)
```

**Waarom werkte dit niet?**

`GameSystemRepository.add_new_system(system)` werd aangeroepen alsof het een static method is, maar `add_new_system` is een **instance method** die een database sessie nodig heeft. Er was geen database connectie beschikbaar!

---

## Wat is een Static Method?

Een `@staticmethod` is een functie die bij een class hoort, maar **geen toegang heeft tot de class of instance**:

```python
class Calculator:
    @staticmethod
    def add(a, b):
        return a + b

# Aanroepen zonder instance te maken:
result = Calculator.add(5, 3)  # result = 8
```

**Kenmerken:**
- Geen `self` parameter
- Geen toegang tot instance variabelen
- Geen toegang tot class variabelen
- Basically gewoon een losse functie die toevallig in een class zit

**Wanneer gebruiken?**
- Pure utility functies die geen state nodig hebben
- Mappers (zoals `GameSystemMapper`) - die transformeren alleen data

**Wanneer NIET gebruiken?**
- Als je een database connectie nodig hebt
- Als je andere services nodig hebt
- Als je state moet bijhouden

---

## Wat is een Class Method?

Een `@classmethod` heeft toegang tot de **class zelf** (niet de instance):

```python
class User:
    count = 0  # Class variabele
    
    def __init__(self, name):
        self.name = name
        User.count += 1
    
    @classmethod
    def get_user_count(cls):
        return cls.count
    
    @classmethod
    def create_admin(cls):
        return cls("Admin")  # Maakt een nieuwe User instance

# Gebruik:
admin = User.create_admin()
print(User.get_user_count())  # 1
```

**Kenmerken:**
- Eerste parameter is `cls` (de class zelf)
- Kan class variabelen lezen/schrijven
- Kan nieuwe instances maken van de class
- Wordt vaak gebruikt als "factory method"

**Wanneer gebruiken?**
- Factory methods (alternatieve constructors)
- Als je class-level state nodig hebt

---

## Wat is Dependency Injection?

Dependency Injection betekent: **geef de dependencies mee in plaats van ze zelf te maken**.

### Zonder DI (slecht):

```python
class GameSystemService:
    def add_system(self):
        db = create_database_connection()  # ❌ Service maakt zelf connectie
        repository = GameSystemRepository(db)   # ❌ Service maakt zelf repository
        # ...
```

### Met DI (goed):

```python
class GameSystemService:
    def __init__(self, repository: GameSystemRepository):
        self.repository = repository  # ✅ Repository wordt meegegeven
    
    def add_system(self, api_system):
        # ✅ Gebruikt de meegegeven repository
        return self.repository.add_new_system(...)
```

**Het idee:** De service weet niet HOE de repository gemaakt wordt. Hij krijgt hem gewoon.

---

## Hoe werkt Depends() in FastAPI?

FastAPI heeft een ingebouwd dependency injection systeem via `Depends()`.

### Stap 1: Definieer dependency functies

```python
# app/dependencies.py

def get_db():
    """Maakt database sessie, sluit hem na de request"""
    db = SessionLocal()
    try:
        yield db  # Geef sessie aan de caller
    finally:
        db.close()  # Cleanup na de request

def get_system_repository(db: Session = Depends(get_db)) -> GameSystemRepository:
    """Maakt repository met database sessie"""
    return GameSystemRepository(db)

def get_system_service(
    repository: GameSystemRepository = Depends(get_system_repository)
) -> GameSystemService:
    """Maakt service met repository"""
    return GameSystemService(repository)
```

### Stap 2: Gebruik in router

```python
# app/routers/game_system_router.py

@router.post("/add-system")
def post_add_system(
    api_system: APIGameSystem,
    service: GameSystemService = Depends(get_system_service)  # FastAPI injecteert dit!
):
    return service.add_system(api_system)
```

### Wat gebeurt er als een request binnenkomt?

```
1. Request komt binnen: POST /system/add-system

2. FastAPI ziet: Depends(get_system_service)
   
3. FastAPI roept get_system_service() aan
   → Die heeft Depends(get_system_repository)
   
4. FastAPI roept get_system_repository() aan
   → Die heeft Depends(get_db)
   
5. FastAPI roept get_db() aan
   → Maakt database sessie
   → yield db (geeft sessie terug, wacht op cleanup)

6. get_system_repository() ontvangt db
   → return GameSystemRepository(db)

7. get_system_service() ontvangt repository
   → return GameSystemService(repository)

8. post_add_system() ontvangt service
   → Voert logica uit
   → Return response

9. Request is klaar
   → FastAPI roept cleanup aan
   → get_db() finally block: db.close()
```

### Waarom `yield` in get_db()?

```python
def get_db():
    db = SessionLocal()
    try:
        yield db      # ← Hier stopt de functie, geeft db terug
    finally:
        db.close()    # ← Dit wordt ALTIJD uitgevoerd na de request
```

`yield` maakt het een **generator function**. FastAPI:
1. Roept `next()` aan om de `db` te krijgen
2. Gebruikt de `db` voor de hele request
3. Na de request: roept cleanup aan (finally block)

Dit is vergelijkbaar met Spring's `@Transactional` of Java's try-with-resources.

---

## De Wijzigingen die we hebben gemaakt

### 1. Nieuw bestand: `app/dependencies.py`

```python
from fastapi import Depends
from sqlalchemy.orm import Session
from app.db import get_db
from app.repositories import GameSystemRepository
from app.services import GameSystemService


def get_system_repository(db: Session = Depends(get_db)) -> GameSystemRepository:
    return GameSystemRepository(db)


def get_system_service(
        repository: GameSystemRepository = Depends(get_system_repository)
) -> GameSystemService:
    return GameSystemService(repository)
```

### 2. Aangepast: `app/services/system_service.py`

**Oud:**

```python
class GameSystemService:
    @staticmethod
    def add_system(api_system: APIGameSystem) -> APIGameSystemResponse:
        system = GameSystemMapper.api_system_to_system(api_system)
        GameSystemRepository.add_new_system(system)  # ❌ Broken
        return GameSystemMapper.game_system_to_api_game_system_response(system)
```

**Nieuw:**

```python
class GameSystemService:
    def __init__(self, repository: GameSystemRepository):
        self.repository = repository

    def add_system(self, api_system: APIGameSystem) -> APIGameSystemResponse:
        system = GameSystemMapper.api_system_to_system(api_system)
        created_system = self.repository.add_new_system(system)  # ✅ Werkt!
        return GameSystemMapper.game_system_to_api_game_system_response(created_system)
```

### 3. Aangepast: `app/routers/system_router.py`

**Oud:**
```python
class SystemRouter:
    router = APIRouter()

    @staticmethod
    @router.post("/add-system", response_model=APIGameSystemResponse)
    def post_add_system(api_system: APIGameSystem):
        return GameSystemService.add_system(api_system)  # ❌ Static call
```

**Nieuw:**
```python
class SystemRouter:
    router = APIRouter()

    @router.post("/add-system", response_model=APIGameSystemResponse)
    def post_add_system(
        api_system: APIGameSystem,
        service: GameSystemService = Depends(get_system_service)  # ✅ Injected
    ):
        return service.add_system(api_system)
```

### 4. Aangepast: `main.py`

**Oud:**
```python
system_router_instance = SystemRouter()  # ❌ Onnodig
app.include_router(system_router_instance.router, prefix="/system", tags=["systems"])
```

**Nieuw:**
```python
app.include_router(SystemRouter.router, prefix="/system", tags=["systems"])  # ✅ Direct
```

---

## Vergelijking met Spring Boot

Als je Spring Boot gewend bent, hier de vergelijking:

| Spring Boot | FastAPI |
|-------------|---------|
| `@Service` annotatie | Gewone class (geen annotatie nodig) |
| `@Repository` annotatie | Gewone class |
| `@Autowired` of constructor injection | `Depends(get_x)` parameter |
| Spring scant en maakt beans automatisch | Jij schrijft dependency functies |
| Singleton scope (default) | Request scope (nieuwe instance per request) |
| `@Transactional` | `yield` in dependency functie |

### Spring Boot voorbeeld:

```java
@Service
public class GameSystemService {
    private final GameSystemRepository repository;
    
    // Spring injecteert automatisch
    public GameSystemService(GameSystemRepository repository) {
        this.repository = repository;
    }
}
```

### FastAPI equivalent:

```python
# De service class
class GameSystemService:
    def __init__(self, repository: GameSystemRepository):
        self.repository = repository

# De dependency functie (dit is wat Spring automatisch doet)
def get_system_service(
    repository: GameSystemRepository = Depends(get_system_repository)
) -> GameSystemService:
    return GameSystemService(repository)
```

**Het verschil:** In Spring Boot is DI "magisch" (automatisch). In FastAPI is het **expliciet** — jij schrijft de functies die dependencies maken. Dit is bewust zo ontworpen: "Explicit is better than implicit" (Python filosofie).

---

## Voordelen van Dependency Injection

### 1. Testbaarheid

Je kunt makkelijk mock objects injecteren voor tests:

```python
def test_add_system():
    # Maak een mock repository
    mock_repo = Mock(spec=GameSystemRepository)
    mock_repo.add_new_system.return_value = System(id=1, name="Test")
    
    # Injecteer de mock
    service = GameSystemService(mock_repo)
    
    # Test
    result = service.add_system(APIGameSystem(name="Test", description="Test"))
    
    # Verify
    mock_repo.add_new_system.assert_called_once()
```

### 2. Losse Koppeling

De service weet niet:
- Welke database je gebruikt
- Hoe de connectie gemaakt wordt
- Welke repository implementatie je gebruikt

Je kunt alles vervangen zonder de service aan te passen.

### 3. Lifecycle Management

FastAPI beheert de lifecycle:
- Database sessies worden automatisch gesloten
- Geen memory leaks
- Geen vergeten `db.close()` calls

### 4. Request Isolation

Elke request krijgt zijn eigen:
- Database sessie
- Repository instance
- Service instance

Geen concurrency problemen door gedeelde state.

### 5. Duidelijke Dependencies

Je ziet direct wat een functie nodig heeft:

```python
def post_add_system(
    api_system: APIGameSystem,
    service: GameSystemService = Depends(get_system_service)  # ← Duidelijk!
):
```

---

## Wanneer WEL @staticmethod gebruiken?

`@staticmethod` is prima voor **pure functies** zonder side effects:

```python
class GameSystemMapper:
    @staticmethod
    def api_system_to_system(api_system: APIGameSystem) -> System:
        # Pure transformatie, geen database, geen state
        return System(name=api_system.name, description=api_system.description)
    
    @staticmethod
    def system_to_api_system_response(system: System) -> APIGameSystemResponse:
        # Pure transformatie
        return APIGameSystemResponse(
            id=system.id,
            name=system.name,
            description=system.description
        )
```

Deze mappers:
- Hebben geen dependencies nodig
- Hebben geen side effects
- Transformeren alleen data

Daarom zijn ze prima als `@staticmethod`.

---

## Samenvatting

| Concept | Wanneer gebruiken |
|---------|-------------------|
| `@staticmethod` | Pure utility functies, mappers |
| `@classmethod` | Factory methods, class-level operations |
| Instance methods + DI | Services, repositories, alles met dependencies |

**De dependency chain:**

```
Request
    ↓
Router (met Depends)
    ↓
get_system_service()
    ↓
get_system_repository()
    ↓
get_db()
    ↓
Database Sessie
```

**Belangrijkste les:** Als je iets nodig hebt (database, andere service, config), laat het injecteren via `Depends()`. Maak het niet zelf aan in de class.

---

## Vragen?

Als je vragen hebt, kijk dan naar:
- FastAPI docs: https://fastapi.tiangolo.com/tutorial/dependencies/
- De `app/dependencies.py` file in dit project
- De gewijzigde services en routers

Succes! 🚀
