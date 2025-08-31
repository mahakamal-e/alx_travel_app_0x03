# ALX Travel App 0x00

A Django REST Framework project for booking travel listings, including user roles (guest/host), booking management, and reviews. This is a duplicate of the original `alx_travel_app` project, enhanced with model definitions, API serializers, and a database seeder command.

---

## 📁 Project Structure

- `listings/models.py`: Contains models for `User`, `Listing`, `Booking`, and `Review`.
- `listings/serializers.py`: Serializers for transforming model data into JSON for the API.
- `listings/management/commands/seed.py`: Command to populate the database with sample data.

---

## 🧱 Models Overview

### 1. `User` (Custom User Model)
- Inherits from `AbstractUser`
- UUID as primary key
- Fields: `phone`, `role` (guest/host), `email` (unique)
- Used for both guests and hosts

### 2. `Listing`
- Represents a place to stay
- Fields: `title`, `description`, `location`, `price_per_night`, `host` (FK to `User`)
- Host owns multiple listings

### 3. `Booking`
- Represents a user's reservation of a listing
- Fields: `user`, `listing`, `check_in_date`, `check_out_date`, `total_price`, `status`
- Linked to `User` and `Listing`

### 4. `Review`
- User feedback on a listing
- Fields: `user`, `listing`, `rating`, `comment`
- Each user can only review the same listing once (`unique_together` constraint)

---

## 🧰 Setup Instructions

### 1. Clone the Project

```bash
git clone 
cd alx_travel_app_0x00