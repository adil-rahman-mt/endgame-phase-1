# Coin–Duty–KSB Management API

This Flask API manages apprenticeship Coins, Duties, and KSBs, and their relationships.

## Data Model

- Coins
- Duties
- KSB

Relationships:

- Coins ↔ Duties (many-to-many)
- Duties ↔ KSB (many-to-many)

Join tables:

- coin_duties
- ksb_duties

## API version 1

### Coins

| Method | Endpoint | Description | Success |
|--------|----------|-------------|---------|
| POST | `/api/v1/coins` | Create coin | 201 |
| GET | `/api/v1/coins` | List all coins | 200 |
| GET | `/api/v1/coins/{id}` | Get a coin | 200 |
| PATCH | `/api/v1/coins/{id}` | Update coin | 200 |
| DELETE | `/api/v1/coins/{id}` | Delete coin | 200 |

### Example request payloads

**POST** `/api/v1/coins`

Required JSON body:

```json
{
  "name": "Automate"
}

```

**PATCH** `/api/v1/coins/{id}`

Required JSON body:

```json
{
  "name": "Security"
}

```

### Duties

| Method | Endpoint | Description | Success |
|--------|----------|-------------|---------|
| POST | `/api/v1/duties` | Create duty | 201 |
| GET | `/api/v1/duties` | List all duties | 200 |
| GET | `/api/v1/duties/{id}` | Get a duty | 200 |
| PATCH | `/api/v1/duties/{id}` | Update duty | 200 |
| DELETE | `/api/v1/duties/{id}` | Delete duty | 200

### Example request payloads

**POST** `/api/v1/duties`

Required JSON body:

```json
{
  "name": "Duty 1",
  "description": "Script and code in at least one general purpose language."
}

```

**PATCH** `/api/v1/duties/{id}`

Partial updates supported — only include fields you want to modify.

```json
{
  "description": "Script and code in at least one general purpose language and at least one domain-specific language to orchestrate infrastructure, follow test driven development and ensure appropriate test coverage."
}

```

### KSB

| Method | Endpoint | Description | Success |
|--------|----------|-------------|---------|
| POST | `/api/v1/ksb` | Create ksb | 201 |
| GET | `/api/v1/ksb` | List all ksb | 200 |
| GET | `/api/v1/ksb/{id}` | Get a ksb | 200 |
| PATCH | `/api/v1/ksb/{id}` | Update ksb | 200 |
| DELETE | `/api/v1/ksb/{id}` | Delete ksb | 200

### Example request payloads

**POST** `/api/v1/ksb`

Type must be one of "Knowledge", "Skill", or "Behaviour"

Required JSON body:

```json
{
  "type": "Knowledge",
  "name": "K1",
  "description": "Continuous Integration."
}

```

**PATCH** `/api/v1/ksb/{id}`

Partial updates supported — only include fields you want to modify.

```json
{
  "description": "Continuous Integration - the benefits of frequent merging of code, the creation of build artefacts and ensuring all tests pass, with automation throughout - including common tooling."
}

```

### Coin–Duty Relationships

| Method | Endpoint | Description | Success |
|--------|----------|-------------|---------|
| POST | `/api/v1/coins/{coin_id}/duties/{duty_id}` | Assign duty to coin | 201 |
| DELETE | `/api/v1/coins/{coin_id}/duties/{duty_id}` | Remove duty from coin | 200 |
| GET | `/api/v1/coins/{coin_id}/duties` | List duties for coin | 200 |

### KSB-Duty Relationships

| Method | Endpoint | Description | Success |
|--------|----------|-------------|---------|
| POST | `/api/v1/duties/{duty_id}/ksb/{ksb_id}` | Assign KSB to duty | 201 |
| DELETE | `/api/v1/duties/{duty_id}/ksb/{ksb_id}` | Remove KSB from duty | 200 |
| GET | `/api/v1/duties/{duty_id}/ksb` | List KSBs for duty | 200 |

## API version 2

### Duties

| Method | Endpoint | Description | Success |
|--------|----------|-------------|---------|
| GET | `/api/v2/duties/{name}` | List all coins associated with duty | 200 |

### KSB

| Method | Endpoint | Description | Success |
|--------|----------|-------------|---------|
| GET | `/api/v2/ksb/{name}` | List all duties associated with KSB | 200 |


## Response Codes

- 200 OK – Successful request with response body
- 201 Created – Resource created
- 400 Bad Request – Invalid input (e.g. invalid UUID)
- 404 Not Found – Resource or relationship not found
- 409 Conflict – Duplicate relationship or constraint violation

