class Category(object):
    
    def __init__(self, category_init=""):
        self.category_name = category_init
        self.ledger = []
        self.expenses = 0.0
        self.expense_percent = 0
        
    def __repr__(self):
        total = 0.00
        header = "**************RR**************".replace("RR", self.category_name)
        header_trim = int((len(header) - 30) // 2)
        header = header[header_trim:-header_trim]
        
        category_summary = header + "\n"

        for item in self.ledger:
            description = item["description"] + (" " * 24)
            description = description[:23]
            amount = float(item["amount"])
            total += amount
            amount = "{:.2f}".format(amount)
            amount = (7 - len(amount)) * " " + amount
            category_summary += description + amount + "\n"
              
        total = "{:.2f}".format(total)   
        category_summary += f"Total: {total}"
        return category_summary
        
    def check_funds(self, amount):
        balance = 0.0
        for dict in self.ledger:
            balance += float(dict["amount"])
        if (balance - amount) >= 0.0:
            return True
        else:
            return False
        
    def deposit(self, amount, description=""):
        new_deposit = {"amount": amount, "description": description}
        self.ledger.append(new_deposit)
        
    def withdraw(self, amount, description=""):
        if self.check_funds(float(amount)) == True:
            withdrawl_amount = "-" + str(amount)
            new_withdrawl = {"amount": float(withdrawl_amount), "description": description}
            self.ledger.append(new_withdrawl)
            return True
        else: 
            return False

    def get_balance(self):
        balance = 0.0
        for dict in self.ledger:
            balance += float(dict["amount"]) 
        return balance    
        
    def transfer(self, amount, new_category):
        if self.check_funds(float(amount)) == True:
            transfer_amount = "-" + str(amount)
            transfer_from = {"amount": float(transfer_amount), "description": f"Transfer to {new_category.category_name}"}
            self.ledger.append(transfer_from)
            transfer_to = {"amount": float(amount), "description": f"Transfer from {self.category_name}"}
            new_category.ledger.append(transfer_to)
            return True
        else:
            return False
        
def isfloat(num):
    try:
        float(num)
        return True
    except ValueError:
        return False
    
def calc_percentage(expense, total_expenses):
    raw_percentage = int((expense / total_expenses) * 100)
    if len(str(raw_percentage)) >= 2:
        rounded_percentage = str(raw_percentage)[0:1] + "0"
    elif len(str(raw_percentage)) < 2:
        rounded_percentage = 0
    return int(rounded_percentage)
    
                    
def create_spend_chart(categories=[]):
    expenses_list = []
    categories_list = []
    total_expenses = 0.0
    for category in categories:
        categories_list.append(category.category_name) 
        for dic in category.ledger:
            for k, v in dic.items():
                if isfloat(v) == True:
                    if v < 0:
                        expenses_stripped = float(str(v).lstrip("-"))
                        expenses_list.append(expenses_stripped)
                        category.expenses += expenses_stripped
    
    rowtop = "Percentage spent by category"              
    spend_table_dict = {
        100: "100|",
        90 : " 90|",
        80 : " 80|",
        70 : " 70|",
        60 : " 60|",
        50 : " 50|",
        40 : " 40|",
        30 : " 30|",
        20 : " 20|",
        10 : " 10|",
        0  : "  0|",
    }  
    rowbot = "    -" + ("---" * len(categories_list))
    row_length = len(rowbot)
                
    total_expenses = sum(expenses_list)
    for category in categories:
        category.expense_percent = calc_percentage(category.expenses, total_expenses)
        for percent, string in spend_table_dict.items():
            if percent <= category.expense_percent:
                spend_table_dict[percent] = string + " o "
            else:
                spend_table_dict[percent] = string + "   "
    
    name_row_count = 0      
    for item in categories_list:
        if len(item) > name_row_count:
            name_row_count = len(item)
            
    name_rows = []   
    for row in range(name_row_count):
        row_string = "     "
        for item in categories_list:
            if  (row + 1) > len(item):
                row_string += "   "   
            else:
                row_string += item[row] + "  "
        name_rows.append(row_string)
    
    spent_chart = rowtop + "\n"
    for key, row in spend_table_dict.items():
        row_spaces = int(row_length - len(row))
        spent_chart += row + (" " * row_spaces) + "\n"
    spent_chart += rowbot + "\n"
    for row in name_rows:
        row_spaces = int(row_length - len(row))
        spent_chart += row + (" " * row_spaces) + "\n"
    spent_chart = spent_chart.rstrip("\n")
    
    return spent_chart
        
food = Category("Food")
food.deposit(900, "deposit")
entertainment = Category("Entertainment")
entertainment.deposit(900, "deposit")
business = Category("Business")
business.deposit(900, "deposit")
food.withdraw(105.55)
entertainment.withdraw(33.40)
business.withdraw(10.99)
actual = create_spend_chart([business, food, entertainment])
raw_actual = r"{}".format(actual)
print(raw_actual)
f = open("raw_print.txt", "w")
f.write(raw_actual)
f.close()

expected = "Percentage spent by category\n100|          \n 90|          \n 80|          \n 70|    o     \n 60|    o     \n 50|    o     \n 40|    o     \n 30|    o     \n 20|    o  o  \n 10|    o  o  \n  0| o  o  o  \n    ----------\n     B  F  E  \n     u  o  n  \n     s  o  t  \n     i  d  e  \n     n     r  \n     e     t  \n     s     a  \n     s     i  \n           n  \n           m  \n           e  \n           n  \n           t  "
f2 = open("expected_print.txt", "w")
f2.write(expected)
f2.close()
