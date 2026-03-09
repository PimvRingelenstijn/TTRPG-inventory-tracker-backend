# TTRPG Inventory Tracker — PHP (Laravel) Backend

PHP/Laravel port of the TTRPG inventory tracker backend. Mirrors the Python FastAPI API.

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
