# Domain Entities — Backend

## Entity Relationship

```
Store 1──N AdminUser
Store 1──N Table
Store 1──N Category
Category 1──N Menu
Table 1──N TableSession
TableSession 1──N Order
Order 1──N OrderItem
Order ──> OrderHistory (세션 종료 시 이동)
```

## Entities

### Store
| Field | Type | Constraints |
|-------|------|-------------|
| id | INT (PK) | AUTO_INCREMENT |
| name | VARCHAR(100) | NOT NULL, UNIQUE |
| created_at | DATETIME | NOT NULL |

### AdminUser
| Field | Type | Constraints |
|-------|------|-------------|
| id | INT (PK) | AUTO_INCREMENT |
| store_id | INT (FK→Store) | NOT NULL |
| username | VARCHAR(50) | NOT NULL |
| password_hash | VARCHAR(255) | NOT NULL (bcrypt) |
| created_at | DATETIME | NOT NULL |
| UNIQUE | (store_id, username) | |

### Category
| Field | Type | Constraints |
|-------|------|-------------|
| id | INT (PK) | AUTO_INCREMENT |
| store_id | INT (FK→Store) | NOT NULL |
| name | VARCHAR(50) | NOT NULL |
| sort_order | INT | DEFAULT 0 |

### Menu
| Field | Type | Constraints |
|-------|------|-------------|
| id | INT (PK) | AUTO_INCREMENT |
| store_id | INT (FK→Store) | NOT NULL |
| category_id | INT (FK→Category) | NOT NULL |
| name | VARCHAR(100) | NOT NULL |
| price | INT | NOT NULL, >= 0 |
| description | TEXT | NULLABLE |
| image_url | VARCHAR(500) | NULLABLE |
| sort_order | INT | DEFAULT 0 |
| is_deleted | BOOLEAN | DEFAULT FALSE |
| created_at | DATETIME | NOT NULL |

### Table
| Field | Type | Constraints |
|-------|------|-------------|
| id | INT (PK) | AUTO_INCREMENT |
| store_id | INT (FK→Store) | NOT NULL |
| table_number | INT | NOT NULL |
| password_hash | VARCHAR(255) | NOT NULL (bcrypt) |
| UNIQUE | (store_id, table_number) | |

### TableSession
| Field | Type | Constraints |
|-------|------|-------------|
| id | INT (PK) | AUTO_INCREMENT |
| table_id | INT (FK→Table) | NOT NULL |
| started_at | DATETIME | NOT NULL |
| completed_at | DATETIME | NULLABLE |
| is_active | BOOLEAN | DEFAULT TRUE |

### Order
| Field | Type | Constraints |
|-------|------|-------------|
| id | INT (PK) | AUTO_INCREMENT |
| store_id | INT (FK→Store) | NOT NULL |
| table_id | INT (FK→Table) | NOT NULL |
| session_id | INT (FK→TableSession) | NOT NULL |
| status | ENUM('pending','preparing','completed') | DEFAULT 'pending' |
| total_amount | INT | NOT NULL |
| created_at | DATETIME | NOT NULL |

### OrderItem
| Field | Type | Constraints |
|-------|------|-------------|
| id | INT (PK) | AUTO_INCREMENT |
| order_id | INT (FK→Order) | NOT NULL |
| menu_id | INT (FK→Menu) | NOT NULL |
| menu_name | VARCHAR(100) | NOT NULL (스냅샷) |
| menu_price | INT | NOT NULL (스냅샷) |
| quantity | INT | NOT NULL, >= 1 |
| subtotal | INT | NOT NULL |

### OrderHistory
| Field | Type | Constraints |
|-------|------|-------------|
| id | INT (PK) | AUTO_INCREMENT |
| order_id | INT | NOT NULL |
| store_id | INT | NOT NULL |
| table_id | INT | NOT NULL |
| session_id | INT | NOT NULL |
| status | VARCHAR(20) | NOT NULL |
| total_amount | INT | NOT NULL |
| order_created_at | DATETIME | NOT NULL |
| completed_at | DATETIME | NOT NULL |
| items_json | JSON | NOT NULL |
