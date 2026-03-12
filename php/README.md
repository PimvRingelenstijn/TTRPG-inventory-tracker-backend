# TTRPG Inventory Tracker — PHP (Laravel) Backend

PHP/Laravel port of the TTRPG inventory tracker backend. Mirrors the Python FastAPI API. This document helps Python developers learn PHP by comparing the two implementations.

---

## Python → PHP: How the Port Was Created

The PHP version follows the same **layered architecture** as the Python app. Each Python layer maps to a PHP equivalent:

| Python (FastAPI) | PHP (Laravel) |
|------------------|---------------|
| `main.py` + routers | `routes/api.php` + `bootstrap/app.php` |
| `app/routers/*.py` | `app/Http/Controllers/*.php` |
| `app/services/*.py` | `app/Services/*.php` |
| `app/repositories/*.py` | `app/Repositories/*.php` |
| `app/dbmodels/*.py` (SQLAlchemy) | `app/Models/*.php` (Eloquent) |
| `app/dtos/*.py` (Pydantic) | `app/DTOs/*.php` (readonly classes) |
| `app/mappers/*.py` | `app/Mappers/*.php` |
| `dependencies/*.py` (Depends) | Laravel service container (constructor injection) |

**Conversion approach:** Each Python module was translated 1:1. Business logic in services and repositories stays the same; only syntax and framework APIs change.

---

## Python vs PHP: Similarities and Differences

### Similarities (Coming from Python)

- **Procedural + OOP:** Both support functions and classes. You can write either style.
- **Dynamic typing:** Both are dynamically typed (PHP has optional type hints like Python).
- **Variable naming:** PHP requires `$` prefix (`$name`); Python uses plain names (`name`). Both are mutable by default.
- **Arrays/lists:** `$arr = [1, 2, 3]` (PHP) ≈ `arr = [1, 2, 3]` (Python).
- **Associative arrays:** `['key' => 'value']` (PHP) ≈ `{'key': 'value'}` (Python dict).
- **Named arguments:** Both support them: `new DTO(name: $x, desc: $y)` (PHP 8) ≈ `DTO(name=x, desc=y)` (Python 3).
- **`fn` / lambda:** `fn ($x) => $x * 2` (PHP) ≈ `lambda x: x * 2` (Python).
- **`null` / `None`:** PHP uses `null`; Python uses `None`.
- **`require` / `import`:** PHP `use App\Service` ≈ Python `from app.services import Service`.
- **Namespaces ≈ packages:** `namespace App\Services` ≈ `app.services` module path.

### Differences (What to Watch For)

| Aspect | Python | PHP |
|--------|--------|-----|
| **Blocks** | Indentation (no braces) | Braces `{}` required |
| **Variables** | No prefix | `$` prefix: `$name` |
| **Method calls** | `obj.method()` | `$obj->method()` (arrow, not dot) |
| **Properties** | `obj.attr` | `$obj->attr` |
| **Static methods** | `@staticmethod` / `cls.method()` | `ClassName::method()` |
| **Constants** | `UPPER_CASE` convention | `const UPPER_CASE` or `define()` |
| **Truthiness** | `""`, `[]`, `0` are falsy | `""`, `[]`, `0` are falsy; `"0"` is also falsy |
| **String concat** | `f"{a} and {b}"` or `a + b` | `"$a and $b"` or `$a . $b` |
| **Array access** | `arr[0]`, `dict['key']` | `$arr[0]`, `$arr['key']` |
| **Optional/Nullable** | `Optional[T]` / `T \| None` | `?T` (e.g. `?int`) |
| **Return types** | `def f() -> int:` | `function f(): int` |
| **Constructor** | `def __init__(self, x):` | `public function __construct($x)` |
| **`self` / `this`** | `self` | `$this` |
| **Private** | `_private` (convention) | `private` (enforced) |
| **Readonly** | `@dataclass(frozen=True)` | `readonly` (PHP 8.1+) |
| **File structure** | One class per file optional | One class per file, class name = filename |

### Code Snippets: Side-by-Side

**DTO (Data Transfer Object):**

```python
# Python (Pydantic)
class GameSystemCreateRequest(BaseModel):
    name: str
    description: str
```

```php
// PHP (readonly class)
class GameSystemCreateRequest
{
    public function __construct(
        public readonly string $name,
        public readonly string $description,
    ) {}
}
```

**Service method:**

```python
# Python
def add_game_system(self, api_game_system: GameSystemCreateRequest) -> GameSystemDataResponse:
    game_system = api_game_system_to_db_model(api_game_system)
    created = self.repository.create(game_system.to_dict())
    return db_game_system_to_api_response(created)
```

```php
// PHP
public function addGameSystem(GameSystemCreateRequest $request): GameSystemDataResponse
{
    $attrs = GameSystemMapper::requestToAttributes($request);
    $model = $this->repository->create($attrs);
    return GameSystemMapper::modelToResponse($model);
}
```

**Dependency injection:**

```python
# Python (FastAPI Depends)
def get_all_game_systems(
    game_system_service: GameSystemService = Depends(get_game_system_service)
):
    return game_system_service.get_all_game_systems()
```

```php
// PHP (Laravel constructor injection)
public function __construct(
    private readonly GameSystemService $gameSystemService
) {}

public function index(): JsonResponse
{
    $systems = $this->gameSystemService->getAllGameSystems();
    return response()->json($systems->map(fn ($dto) => $dto->toArray())->values()->all());
}
```

**Validation:** Python uses Pydantic (automatic from request body); PHP uses Laravel's `$request->validate([...])` and then builds DTOs manually.

---

## Requirements

- PHP 8.2+
- Composer
- PostgreSQL (e.g. Supabase)
- Supabase project (for auth)

## Setup

1. Install dependencies:
   ```bash
   composer install
   ```

2. Copy environment file:
   ```bash
   cp .env.example .env
   ```

3. Generate application key:
   ```bash
   php artisan key:generate
   ```

4. Configure `.env`:
   - `DB_*`: PostgreSQL credentials (mirror Python's USER, PASSWORD, HOST, PORT, DBNAME)
   - `SUPABASE_URL`: Supabase project URL
   - `SUPABASE_SERVICE_KEY`: Supabase service role key

5. Run migrations:
   ```bash
   php artisan migrate
   ```
   Note: If using the same database as the Python app, tables may already exist. Use a fresh database or run `php artisan migrate:fresh` (destructive) to recreate.

## Running

```bash
php artisan serve
```

Server runs at `http://127.0.0.1:8000`.

## API Endpoints

| Method | Path | Description |
|--------|------|-------------|
| POST | /auth/register | Register user |
| POST | /auth/login | Login (sets access_token cookie) |
| POST | /auth/logout | Logout (clears cookie) |
| GET | /auth/me | Current user (requires auth) |
| POST | /game-systems | Create game system |
| GET | /game-systems | List game systems |
| GET | /game-systems/{id} | Get game system by ID |

## Testing

```bash
php artisan test
```

## Env Variable Mapping (Python → PHP)

| Python (.env) | PHP (.env) |
|---------------|------------|
| USER | DB_USERNAME |
| PASSWORD | DB_PASSWORD |
| HOST | DB_HOST |
| PORT | DB_PORT |
| DBNAME | DB_DATABASE |
| SUPABASE_URL | SUPABASE_URL |
| SUPABASE_SERVICE_KEY | SUPABASE_SERVICE_KEY |

---

## Learning Tip

When exploring this codebase, open the Python and PHP versions side-by-side. Start with `GameSystemController` vs `game_system_router.py`, then follow the flow into `GameSystemService` and `GameSystemRepository`. The structure is identical; only the syntax differs.
