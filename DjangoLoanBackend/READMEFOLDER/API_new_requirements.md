**Beautifully summarized, General.** Here's your updated implementation plan based on that summary — I’ve structured it clearly so your dev team (or future self) can go straight to work:

---

## ✅ **Changes to the Application Entity & Logic**

### 🔧 Add a Predefined Field: `stage`
- Type: `Enum`
- Values:
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
- Triggers:
  - Send **email** to `broker.email` and `borrowers[].email` **when stage changes**
  - Start **timer logic** to track if stage remains the same for `X` days
    - If yes, send **notification** to assigned `bd.email`

---

## ✅ **Broker Detail Page Fields (Frontend & API Response)**

- `name`
- `company`
- `phone`
- `email`
- `branch_id` → Display branch name
- `bd_ids` → Display list of linked BDs (Many-to-Many)

---

## ✅ **New: BD API Service**

### **Endpoints**
| Method | Endpoint             | Description                   |
|--------|----------------------|-------------------------------|
| GET    | `/bds/`              | List all BDs (optional filters) |
| POST   | `/bds/`              | Create a BD                   |
| GET    | `/bds/{id}/`         | Get BD detail                 |
| DELETE | `/bds/{id}/`         | Delete BD                     |
| PATCH  | `/bds/{id}/`         | Update BD                     |

### **BD Fields**
- `id`
- `name`
- `email`
- `phone`
- `branch_id`

> ⚠️ Each BD must belong to a **Branch**

---

## ✅ **New: Branch Company API Service**

### **Endpoints**
| Method | Endpoint                | Description                  |
|--------|-------------------------|------------------------------|
| GET    | `/branches/`           | List all branches            |
| POST   | `/branches/`           | Create a new branch          |
| GET    | `/branches/{id}/`      | Get branch detail            |
| DELETE | `/branches/{id}/`      | Delete branch                |
| PATCH  | `/branches/{id}/`      | Update branch info           |

### **Branch Fields**
- `id`
- `name`
- `address`

> ⚠️ A **Branch can have multiple BDs**

---

## ✅ **Data Creation Flow When an Application is Created**

When user fills form or uploads it as PDF:
1. **Create Application**
2. **Create Borrower(s)** (from form — one or more)
3. **Create Company Borrower** (if business loan)
4. **Create Guarantor(s)** (linked to borrower & application)
5. **Create Loan Details**
   - Purpose
   - Loan Amount
   - Term
   - Expected Rate
6. **Create Property/Security Info**
7. **Store Signature block** (or attach scanned form)
8. **Link all above** to Application

---


