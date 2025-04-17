## ✅ Changes to the Application Entity & Logic (Now with Input Fields)

### 🔧 Add a Predefined Field: `stage`

- **Type:** Enum
- **Values:**
  ```
  [
    "enquiry",
    "indicative offer",
    "valuation",
    "dual",
    "formal approval",
    "loan documents issued",
    "loan documents return",
    "settlement",
    "reject",
    "withdrawal"
  ]
  ```
- **Triggers:**
  - Send **email** to `broker.email` and `borrowers[].email` **when stage changes**
  - Timer logic to notify BD if the case stays in same stage for `X` days (configurable)

---

## ✅ Broker Detail Page Fields (Frontend & API Response)

- `name`
- `company`
- `phone`
- `email`
- `branch_id` ➔ Display branch name
- `bd_ids` ➔ Display list of linked BDs (Many-to-Many)

---

## ✅ New: BD API Service

### Endpoints

| Method | Endpoint     | Description                          |
| ------ | ------------ | ------------------------------------ |
| GET    | `/bds/`      | List all BDs (with optional filters) |
| POST   | `/bds/`      | Create a new BD                      |
| GET    | `/bds/{id}/` | Get BD detail                        |
| DELETE | `/bds/{id}/` | Delete BD                            |
| PATCH  | `/bds/{id}/` | Update BD                            |

### Fields

- `id`
- `name`
- `email`
- `phone`
- `branch_id`

> ⚠️ A BD must belong to a Branch
>
> And a BD can belong to different Branch.

---

## ✅ New: Branch Company API Service

### Endpoints

| Method | Endpoint         | Description        |
| ------ | ---------------- | ------------------ |
| GET    | `/branches/`     | List branches      |
| POST   | `/branches/`     | Create new branch  |
| GET    | `/branches/{id}` | Get branch detail  |
| DELETE | `/branches/{id}` | Delete branch      |
| PATCH  | `/branches/{id}` | Update branch info |

### Fields

- `id`
- `name`
- `address`

> ⚠️ A Branch can have multiple BDs

---

## ✅ Data Creation Flow When an Application is Created (with Input Fields)

When a user submits the application form (or uploads PDF):

### 1. 📅 Application

- reference\_number
- application\_type
- purpose
- loan\_amount
- interest\_rate
- loan\_term
- loan\_term\_unit
- repayment\_frequency
- product\_id
- estimated\_settlement\_date
- stage *(enum)*
- bd\_id, branch\_id

### 2. 👨‍💼 Borrower(s)

- first\_name / last\_name / full\_name
- date\_of\_birth / gender / marital\_status
- email / phone / mobile / work\_phone
- residential\_address & mailing\_address (street, unit, city, state, postal\_code, country)
- residential\_status, years\_at\_address, nationality
- tax\_id, id\_type, id\_number, id\_expiry\_date
- dependents
- employment: status, employer name, position, start/end date, phone, address
- banking: bank\_name, account\_type, account\_number, bsb, holder\_name, years\_with\_bank
- financials: income, expenses, assets, liabilities
- additional\_info: notes, tags, referral\_source

### 3. 💼 Company Borrower (if business loan)

- company\_name
- abn / acn
- director\_id
- contact\_number
- industry\_type
- registered\_address (same structure as above)
- trustee\_flags (is\_trustee, is\_smsf)
- trustee\_name
- annual\_income

### 4. 👨‍💼 Guarantor(s)

- first\_name / last\_name / full\_name
- relationship
- email / phone / dob
- address (full structure)
- borrower\_id

### 5. 📉 Loan Details

- purpose (multi-select): purchase, refinance, cash out, etc.
- use\_of\_funds (description & amount per row)
- term & expected rate
- proposed settlement date
- exit\_strategy: sale, refinance, cashflow, other

### 6. 🏠 Security / Property Info

- address: unit/street/suburb/state/postcode
- property\_type (enum)
- estimated\_value
- purchase\_price
- current\_debt: 1st mortgage, 2nd mortgage
- valuation\_type: single/double/garage/etc.
- bedrooms, bathrooms, car\_spaces, building\_size, land\_size
- owner\_occupied (boolean)

### 7. 🛌 Signatures & Upload

- form\_signature\_date
- form\_signed\_by: borrower(s)/guarantor(s)
- uploaded\_pdf\_path (link to stored document)

---

## ✅ Final Valuer + QS Schema

Embedded directly in `Application` input form:

### Input Fields (to be filled manually or extracted from uploaded PDF):

#### Valuer Info
- `valuer_info.company_name`
- `valuer_info.contact_name`
- `valuer_info.email`
- `valuer_info.phone`

#### QS Info
- `qs_info.company_name`
- `qs_info.contact_name`
- `qs_info.email`
- `qs_info.phone`

These fields(QS, Valuer) are:
- ✅ Part of the `Application` object
- ❌ Not managed through separate APIs
- 🔒 Treated as **read-only reference values** after submission (for audit and traceability)

> Simple, flat input blocks instead of separate Valuer/QS models or tables

---

You are now **deployment-ready** with clear input mappings for all entities and API responsibilities.
Let me know when you're ready for the updated backend schema file, API payload mockups, or ER diagram.

