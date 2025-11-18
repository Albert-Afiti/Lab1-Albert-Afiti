#!/usr/bin/env python3
"""
Grade Generator Calculator 
BSE Year 1 Trimester 2 - Lab 1

"""

import csv
from datetime import datetime

class Assignment:
    def __init__(self, name, category, grade, weight):
        self.name = name
        self.category = category.upper()  # Store as uppercase
        self.grade = float(grade)
        self.weight = float(weight)
    
    def calculate_weighted_grade(self):
        """Calculate weighted grade for this assignment"""
        return (self.grade / 100) * self.weight
    
    def to_list(self):
        """Convert assignment to list for CSV export"""
        return [self.name, self.category, f"{self.grade:.2f}", f"{self.weight:.2f}"]

class GradeCalculator:
    def __init__(self, pass_mark=50):
        self.assignments = []
        self.pass_mark = pass_mark
    
    def validate_grade(self, grade):
        """Validate grade is between 0 and 100"""
        try:
            grade_float = float(grade)
            if 0 <= grade_float <= 100:
                return True, grade_float
            else:
                return False, "Grade must be between 0 and 100"
        except ValueError:
            return False, "Grade must be a number"
    
    def validate_weight(self, weight):
        """Validate weight is positive"""
        try:
            weight_float = float(weight)
            if weight_float > 0:
                return True, weight_float
            else:
                return False, "Weight must be a positive number"
        except ValueError:
            return False, "Weight must be a number"
    
    def validate_category(self, category):
        """Validate category is FA or SA"""
        category_upper = category.upper()
        if category_upper in ['FA', 'SA']:
            return True, category_upper
        else:
            return False, "Category must be 'FA' or 'SA'"
    
    def get_user_input(self):
        """Collect and validate user input for an assignment"""
        print("\n" + "==================================================")
        
        # the Assignment Name
        while True:
            name = input("Pleae Enter Assignment Name: ").strip()
            if name:
                break
            print("please Assignment name cannot be empty")
        
        # The Category
        while True:
            category = input("Enter Category (FA for Formative, SA for Summative): ").strip()
            valid, result = self.validate_category(category)
            if valid:
                category = result
                break
            print(result)
        
        #The Grade
        while True:
            grade = input("Please Enter Grade Obtained (0-100): ").strip()
            valid, result = self.validate_grade(grade)
            if valid:
                grade = result
                break
            print(result)
        
        #The Weight
        while True:
            weight = input("Enter Weight: ").strip()
            valid, result = self.validate_weight(weight)
            if valid:
                weight = result
                break
            print(result)
        
        return Assignment(name, category, grade, weight)
    
    def add_assignments(self):
        """Main loop to add multiple assignments"""
        print("=============================")
        print("GRADE GENERATOR CALCULATOR")
        print("=============================")
        
        while True:
            assignment = self.get_user_input()
            self.assignments.append(assignment)
            
            while True:
                continue_input = input("\nAdd another assignment? (y/n): ").strip().lower()
                if continue_input in ['y', 'n', 'yes', 'no']:
                    break
                print("Please enter 'y' or 'n'")
            
            if continue_input in ['n', 'no']:
                break
    
    def calculate_totals(self):
        """Calculate category totals and final grade"""
        fa_total_weighted = 0
        fa_total_weight = 0
        sa_total_weighted = 0
        sa_total_weight = 0
        
        for assignment in self.assignments:
            weighted_grade = assignment.calculate_weighted_grade()
            if assignment.category == 'FA':
                fa_total_weighted += weighted_grade
                fa_total_weight += assignment.weight
            elif assignment.category == 'SA':
                sa_total_weighted += weighted_grade
                sa_total_weight += assignment.weight
        
        # Calculating the  percentages
        fa_percentage = (fa_total_weighted / fa_total_weight * 100) if fa_total_weight > 0 else 0
        sa_percentage = (sa_total_weighted / sa_total_weight * 100) if sa_total_weight > 0 else 0
        
        total_grade = fa_total_weighted + sa_total_weighted
        total_weight = fa_total_weight + sa_total_weight
        
        final_percentage = (total_grade / total_weight * 100) if total_weight > 0 else 0
        gpa = (final_percentage / 100) * 5.0
        
        return {
            'fa_percentage': fa_percentage,
            'sa_percentage': sa_percentage,
            'fa_total_weight': fa_total_weight,
            'sa_total_weight': sa_total_weight,
            'final_percentage': final_percentage,
            'gpa': gpa
        }
    
    def determine_pass_fail(self, fa_percentage, sa_percentage):
        """Determine if student passes based on category requirements"""
        fa_pass = fa_percentage >= self.pass_mark
        sa_pass = sa_percentage >= self.pass_mark
        
        if fa_pass and sa_pass:
            return "PASS", "Congratulations!!! You have passed the course all the best champion."
        else:
            status = "FAIL"
            message = "Sorry You have failed and will repeat the course."
            if not fa_pass and not sa_pass:
                message += " Need to improve both Formative and Summative assignments as soon as possible."
            elif not fa_pass:
                message += " Need to improve Formative assignments."
            else:
                message += " Need to improve Summative assignments."
            return status, message
    
    def display_summary(self):
        """Display comprehensive summary to console"""
        if not self.assignments:
            print("Please no assignments entered.try again.")
            return
        
        calculations = self.calculate_totals()
        status, message = self.determine_pass_fail(
            calculations['fa_percentage'], 
            calculations['sa_percentage']
        )
        
        print("\n" + "==================================")
        print("COURSE TRANSCRIPT SUMMARY")
        print("================================")
        
        # How the individual assignment is displayed
        print("\nASSIGNMENT DETAILS:")
        print("------------------------------------------------------------")
        print(f"{'Assignment Name':<25} {'Category':<10} {'Grade':<8} {'Weight':<8} {'Weighted':<10}")
        print("------------------------------------------------------------")
        
        for assignment in self.assignments:
            weighted = assignment.calculate_weighted_grade()
            print(f"{assignment.name:<25} {assignment.category:<10} {assignment.grade:<8.1f} {assignment.weight:<8.1f} {weighted:<10.2f}")
        
        #how the total category is displayed  
        print("\nCATEGORY TOTALS:")
        print("--------------------")
        print(f"Formative (FA): {calculations['fa_percentage']:.2f}% (Weight: {calculations['fa_total_weight']:.1f})")
        print(f"Summative (SA): {calculations['sa_percentage']:.2f}% (Weight: {calculations['sa_total_weight']:.1f})")
        
        # How the final result is displayed Display 
        print("\nFINAL RESULTS:")
        print("------------------")
        print(f"Final Grade: {calculations['final_percentage']:.2f}%")
        print(f"GPA: {calculations['gpa']:.3f} / 5.0")
        print(f"Status: {status}")
        print(f"Message: {message}")
        print("=================================================================================================")
    
    def export_to_csv(self, filename="grades.csv"):
        """Export all assignment data to CSV file"""
        try:
            with open(filename, 'w', newline='') as csvfile:
                writer = csv.writer(csvfile)
                # Writing the  header
                writer.writerow(['Assignment', 'Category', 'Grade', 'Weight'])
                # Writing the assignment data
                for assignment in self.assignments:
                    writer.writerow(assignment.to_list())
            print(f"\nData successfully exported to {filename}")
            return True
        except Exception as e:
            print(f"Error exporting to CSV: {e}")
            return False

def main():
    """Main function to run the grade calculator"""
    calculator = GradeCalculator()
    
    # Adding  assignments interactively
    calculator.add_assignments()
    
    if not calculator.assignments:
        print("Please no assignments were entered. Exiting. ")
        return
    
    # Displaying  summary
    calculator.display_summary()
    
    # Exporting to CSV
    calculator.export_to_csv()
    print("-------------------------------------------------------")
    print("\nThank you for using the Grade Generator Calculator!")
    print("```````````````````````````````````````````````````````")

if __name__ == "__main__":
    main()
