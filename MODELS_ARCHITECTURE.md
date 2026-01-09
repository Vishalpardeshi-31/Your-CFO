# FinMate Models Architecture

## CustomUser (accounts/models.py) ✅ CREATED

```python
class CustomUser(AbstractUser):
    phone_number = CharField(max_length=15, blank=True)
    profile_picture = ImageField(upload_to='profile_pictures/', blank=True)
    date_of_birth = DateField(blank=True)
    bio = TextField(blank=True)
    onboarding_completed = BooleanField(default=False)
    created_at = DateTimeField(auto_now_add=True)
    updated_at = DateTimeField(auto_now=True)
```

---

## 📊 Suggested Models by App

### **accounts/models.py** (Already has CustomUser)

```python
class UserProfile(models.Model):
    """Extended user profile for financial data"""
    user = OneToOneField(CustomUser, on_delete=CASCADE)
    monthly_income = DecimalField(max_digits=12, decimal_places=2, null=True)
    currency = CharField(max_length=3, default='USD')
    preferred_categories = JSONField(default=list)
    notification_preferences = JSONField()
    created_at = DateTimeField(auto_now_add=True)
    updated_at = DateTimeField(auto_now=True)

class OnboardingStep(models.Model):
    """Track user onboarding progress"""
    user = ForeignKey(CustomUser, on_delete=CASCADE)
    step = CharField(max_length=50)  # 'profile', 'bank', 'goals'
    completed = BooleanField(default=False)
    completed_at = DateTimeField(null=True)
```

---

### **dashboard/models.py**

```python
class Dashboard(models.Model):
    """User dashboard configuration"""
    user = OneToOneField(CustomUser, on_delete=CASCADE)
    layout = CharField(max_length=50, default='default')
    widgets = JSONField()  # Which widgets to display
    theme = CharField(max_length=50, default='light')
    updated_at = DateTimeField(auto_now=True)

class ExpenseCategory(models.Model):
    """Predefined and custom expense categories"""
    name = CharField(max_length=50)
    icon = CharField(max_length=100)
    color = CharField(max_length=7)  # Hex color
    is_default = BooleanField(default=True)
    user = ForeignKey(CustomUser, on_delete=CASCADE, null=True)

class MonthlyBudget(models.Model):
    """User's monthly budget by category"""
    user = ForeignKey(CustomUser, on_delete=CASCADE)
    month = DateField()  # First day of month
    category = ForeignKey(ExpenseCategory, on_delete=CASCADE)
    budget_amount = DecimalField(max_digits=12, decimal_places=2)
    spent_amount = DecimalField(max_digits=12, decimal_places=2, default=0)
    
    class Meta:
        unique_together = ('user', 'month', 'category')
```

---

### **transactions/models.py**

```python
class BankAccount(models.Model):
    """Linked bank accounts for transaction import"""
    user = ForeignKey(CustomUser, on_delete=CASCADE)
    account_name = CharField(max_length=100)
    account_number = CharField(max_length=20)
    bank_name = CharField(max_length=100)
    account_type = CharField(max_length=50)  # 'checking', 'savings'
    balance = DecimalField(max_digits=12, decimal_places=2)
    last_sync = DateTimeField(null=True)
    is_active = BooleanField(default=True)

class Transaction(models.Model):
    """Individual transactions"""
    TRANSACTION_TYPES = (
        ('income', 'Income'),
        ('expense', 'Expense'),
        ('transfer', 'Transfer'),
    )
    
    user = ForeignKey(CustomUser, on_delete=CASCADE)
    bank_account = ForeignKey(BankAccount, on_delete=SET_NULL, null=True)
    transaction_date = DateField()
    amount = DecimalField(max_digits=12, decimal_places=2)
    description = CharField(max_length=255)
    category = ForeignKey(ExpenseCategory, on_delete=SET_NULL, null=True)
    transaction_type = CharField(max_length=20, choices=TRANSACTION_TYPES)
    merchant = CharField(max_length=255, blank=True)
    tags = JSONField(default=list)
    notes = TextField(blank=True)
    created_at = DateTimeField(auto_now_add=True)
    updated_at = DateTimeField(auto_now=True)

class BankStatement(models.Model):
    """Uploaded bank statements"""
    user = ForeignKey(CustomUser, on_delete=CASCADE)
    bank_account = ForeignKey(BankAccount, on_delete=CASCADE)
    file = FileField(upload_to='statements/%Y/%m/')
    file_type = CharField(max_length=10)  # 'csv', 'xlsx'
    statement_date = DateField()
    start_date = DateField()
    end_date = DateField()
    transaction_count = IntegerField()
    status = CharField(max_length=20, default='pending')  # 'pending', 'processed', 'failed'
    error_message = TextField(blank=True)
    uploaded_at = DateTimeField(auto_now_add=True)
    processed_at = DateTimeField(null=True)

class TransactionRecurring(models.Model):
    """Track recurring transactions (subscriptions, bills)"""
    user = ForeignKey(CustomUser, on_delete=CASCADE)
    name = CharField(max_length=100)
    amount = DecimalField(max_digits=12, decimal_places=2)
    frequency = CharField(max_length=20)  # 'weekly', 'monthly', 'yearly'
    start_date = DateField()
    end_date = DateField(null=True)
    category = ForeignKey(ExpenseCategory, on_delete=SET_NULL, null=True)
    is_active = BooleanField(default=True)
```

---

### **goals/models.py**

```python
class Goal(models.Model):
    """Financial goals for future planning"""
    GOAL_CATEGORIES = (
        ('savings', 'Savings'),
        ('investment', 'Investment'),
        ('debt_payoff', 'Debt Payoff'),
        ('education', 'Education'),
        ('travel', 'Travel'),
        ('home', 'Home'),
        ('retirement', 'Retirement'),
        ('other', 'Other'),
    )
    
    user = ForeignKey(CustomUser, on_delete=CASCADE)
    name = CharField(max_length=100)
    description = TextField(blank=True)
    category = CharField(max_length=20, choices=GOAL_CATEGORIES)
    target_amount = DecimalField(max_digits=12, decimal_places=2)
    current_amount = DecimalField(max_digits=12, decimal_places=2, default=0)
    start_date = DateField()
    target_date = DateField()
    priority = CharField(max_length=20, choices=(('low', 'Low'), ('medium', 'Medium'), ('high', 'High')))
    status = CharField(max_length=20, default='active')  # 'active', 'completed', 'abandoned'
    created_at = DateTimeField(auto_now_add=True)
    updated_at = DateTimeField(auto_now=True)
    
    @property
    def progress_percentage(self):
        if self.target_amount == 0:
            return 0
        return (self.current_amount / self.target_amount) * 100

class GoalContribution(models.Model):
    """Contributions towards a goal"""
    goal = ForeignKey(Goal, on_delete=CASCADE)
    amount = DecimalField(max_digits=12, decimal_places=2)
    date = DateField()
    note = CharField(max_length=255, blank=True)
    transaction = ForeignKey(Transaction, on_delete=SET_NULL, null=True, blank=True)
    created_at = DateTimeField(auto_now_add=True)

class GoalMilestone(models.Model):
    """Milestones within a goal"""
    goal = ForeignKey(Goal, on_delete=CASCADE)
    name = CharField(max_length=100)
    target_amount = DecimalField(max_digits=12, decimal_places=2)
    target_date = DateField()
    completed = BooleanField(default=False)
    completed_at = DateTimeField(null=True)
```

---

### **agents/models.py**

```python
class AIInsight(models.Model):
    """AI-generated financial insights"""
    INSIGHT_TYPES = (
        ('spending_pattern', 'Spending Pattern'),
        ('savings_opportunity', 'Savings Opportunity'),
        ('anomaly_detected', 'Anomaly Detected'),
        ('goal_progress', 'Goal Progress'),
        ('recommendation', 'Recommendation'),
        ('alert', 'Alert'),
    )
    
    user = ForeignKey(CustomUser, on_delete=CASCADE)
    insight_type = CharField(max_length=30, choices=INSIGHT_TYPES)
    title = CharField(max_length=255)
    description = TextField()
    data = JSONField()  # Additional data/metrics
    severity = CharField(max_length=20, default='info')  # 'info', 'warning', 'critical'
    actionable = BooleanField(default=True)
    dismissed = BooleanField(default=False)
    created_at = DateTimeField(auto_now_add=True)

class SpendingAnalysis(models.Model):
    """Monthly spending analysis and trends"""
    user = ForeignKey(CustomUser, on_delete=CASCADE)
    month = DateField()  # First day of month
    total_income = DecimalField(max_digits=12, decimal_places=2)
    total_expenses = DecimalField(max_digits=12, decimal_places=2)
    savings = DecimalField(max_digits=12, decimal_places=2)
    savings_rate = DecimalField(max_digits=5, decimal_places=2)  # Percentage
    category_breakdown = JSONField()  # {category: amount}
    trend_vs_previous = JSONField()  # Comparison with previous month
    generated_at = DateTimeField(auto_now_add=True)

class Recommendation(models.Model):
    """AI-generated financial recommendations"""
    user = ForeignKey(CustomUser, on_delete=CASCADE)
    category = CharField(max_length=50)
    title = CharField(max_length=255)
    description = TextField()
    action = CharField(max_length=255)  # Suggested action
    potential_savings = DecimalField(max_digits=12, decimal_places=2, null=True)
    confidence_score = DecimalField(max_digits=3, decimal_places=2)  # 0-1
    accepted = BooleanField(default=False)
    created_at = DateTimeField(auto_now_add=True)
    updated_at = DateTimeField(auto_now=True)

class TransactionAnomaly(models.Model):
    """Detected unusual transactions"""
    user = ForeignKey(CustomUser, on_delete=CASCADE)
    transaction = ForeignKey(Transaction, on_delete=CASCADE)
    anomaly_type = CharField(max_length=50)  # 'unusual_amount', 'new_merchant'
    confidence = DecimalField(max_digits=3, decimal_places=2)  # Confidence score
    description = TextField()
    reviewed = BooleanField(default=False)
    is_legitimate = BooleanField(null=True)  # User feedback
    created_at = DateTimeField(auto_now_add=True)

class FinancialHealthScore(models.Model):
    """Overall financial health assessment"""
    user = ForeignKey(CustomUser, on_delete=CASCADE)
    score = IntegerField()  # 0-100
    categories = JSONField()  # {category: score}
    savings_health = IntegerField()
    debt_health = IntegerField()
    investment_health = IntegerField()
    goal_progress = IntegerField()
    generated_at = DateTimeField(auto_now_add=True)
```

---

## 🔗 Model Relationships Diagram

```
CustomUser (accounts)
    ├── UserProfile (1:1)
    ├── OnboardingStep (1:M)
    ├── Dashboard (1:1)
    ├── BankAccount (1:M)
    ├── Transaction (1:M)
    ├── BankStatement (1:M)
    ├── TransactionRecurring (1:M)
    ├── Goal (1:M)
    │   ├── GoalContribution (1:M)
    │   └── GoalMilestone (1:M)
    ├── AIInsight (1:M)
    ├── SpendingAnalysis (1:M)
    ├── Recommendation (1:M)
    ├── TransactionAnomaly (1:M)
    └── FinancialHealthScore (1:M)

ExpenseCategory (dashboard)
    ├── Transaction (1:M) [foreign key]
    ├── MonthlyBudget (1:M) [foreign key]
    └── TransactionRecurring (1:M) [foreign key]

BankAccount (transactions)
    ├── Transaction (1:M)
    └── BankStatement (1:M)

Transaction (transactions)
    ├── TransactionRecurring (1:M) [link]
    ├── GoalContribution (1:M) [foreign key]
    └── TransactionAnomaly (1:M) [foreign key]

Goal (goals)
    ├── GoalContribution (1:M)
    └── GoalMilestone (1:M)
```

---

## 📝 Implementation Steps

### 1. Start with Core Models
```python
# Phase 1: Basic structure
- CustomUser ✅
- UserProfile
- ExpenseCategory
- BankAccount
- Transaction
- Goal
```

### 2. Add Analytics Models
```python
# Phase 2: Analytics & aggregation
- MonthlyBudget
- Dashboard
- SpendingAnalysis
```

### 3. Add Advanced Features
```python
# Phase 3: AI & recommendations
- AIInsight
- Recommendation
- TransactionAnomaly
- FinancialHealthScore
```

---

## 💡 Key Design Decisions

1. **CustomUser vs Separate Profile**: CustomUser is used as the auth model for simplicity. UserProfile is optional for additional fields.

2. **JSONField for Flexibility**: Categories, preferences, and complex data use JSONField for flexibility without additional tables.

3. **Denormalization for Performance**: Fields like `current_amount`, `spent_amount`, `total_expenses` are denormalized for faster queries.

4. **Soft Deletes**: Consider adding an `is_deleted` BooleanField instead of hard deletes for audit trails.

5. **Audit Trail**: Add `created_by`, `updated_by` fields for transaction tracking in admin apps.

---

## 🔧 Migration Strategy

```bash
# Create migrations for each app
python manage.py makemigrations accounts
python manage.py makemigrations dashboard
python manage.py makemigrations transactions
python manage.py makemigrations goals
python manage.py makemigrations agents

# Apply all migrations
python manage.py migrate

# View migration status
python manage.py showmigrations
```

---

Ready to implement these models! 🚀
