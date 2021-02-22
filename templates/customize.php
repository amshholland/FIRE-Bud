{% extends "layout.html" %}
 
{% block title %}
Customize Budget
{% endblock %}
 
{% block main %}
 
 
<h1 class="h1">Customize Your Budget</h1>
 
<form method="POST" action="customized.php">
    <h2 class="h2">What day of the month do you want to budget?</h2>
    <input name="day" placeholder="Day" type="text">    
    <input name="id" value='1' type="hidden">
 
    <h2 class="h2">Income</h2>
 
    <script>
        // Dynamically add and remove rows
        $(document).ready(function () {
            // Variables
            var newrow = '<p /><div><input type="hidden" name="in_id[]" id="childin_id" value="{{ id }}"><input type="hidden" name="income[]" id="childincome" value="income"><input type="text" name="in_type[]" id="childin_type" placeholder="Income Type" /><input type="text" name="in_amount[]" id="childin_amount" placeholder="Expected Amount" /><input type="date" name="in_date[]" id="childin_date" placeholder="Date" /><input type="button" id="in_remove" value="X" /></div>';
 
            // Add rows to form
            $("#in_add").click(function () {
                $("#income").append(newrow);
            });
 
            // Remove rows from form
            $("#income").on("click", "#in_remove", function () {
                $(this).parent("div").remove();
            });
        });
    </script>
 
    <div id="income">
        <input type="hidden" name="in_id[]" id="in_id" value="1">
        <input type="hidden" name="income[]" id="income" value="income">
        <input type="text" name="in_type[]" id="in_type" placeholder="Income Type" />
        <input type="text" name="in_amount[]" id="in_amount" placeholder="Expected Amount" />
        <input type="date" name="in_date[]" id="in_date" placeholder="Date" />
        <input type="button" id="in_add" value="Add More" />
    </div>
 
    <h2 class="h2">Expenses</h2>
 
    <script>
        // Dynamically add and remove category text boxes
        $(document).ready(function () {
            // Variables
            var newrow = '<p /><div><input type="hidden" name="ex_id[]" id="childex_id" value="{{ id }}"><input type="hidden" name="expense[]" id="childexpense" value="expense"><p /><div><input type="text" name="ex_type[]" id="childex_type" placeholder="Expense Category" /><input type="text" name="ex_amount[]" id="childex_amount" placeholder="Budgeted Amount" /><input type="button" id="remove_cat" value="X" /></div>';
 
            // Add rows to form
            $("#add_cat").click(function () {
                $("#category").append(newrow);
            });
 
            // Remove rows from form
            $("#category").on("click", "#remove_cat", function () {
                $(this).parent("div").remove();
            });
        });
    </script>
 
    <div id="category">
        <input type="hidden" name="ex_id[]" value="{{ id }}">
        <input type="hidden" name="expense[]" value="expense">
        <input type="text" name="ex_type[]" id="ex_type" placeholder="Expense Catagory" />
        <input type="text" name="ex_amount[]" id="ex_amount" placeholder="Budgeted Amount" />
        <input type="button" id="add_cat" value="Add More" />
    </div>
 
    <h2 class="h2">Monthly Bills</h2>
 
    <script>
        // Dynamically add and remove bills text boxes
        $(document).ready(function () {
            // Variables
            var newrow = '<input type="hidden" name="ex_id[]" id="childex_id" value="{{ id }}"><input type="hidden" name="expense[]" id="childexpense" value="expense"><p /><div><input type="text" name="ex_type[]" id="childex_type" placeholder="Bill" /><input type="text" name="ex_amount[]" id="childex_amount" placeholder="Estimated Bill Total" /><input type="date" name="ex_due[]" id="childex_due" placeholder="Payment Due" /><input type="button" id="remove_bill" value="X" /></div>';
 
            // Add row to form
            $("#add_bill").click(function () {
                $("#bills").append(newrow);
            });
 
            // Remove row from form
            $("#bills").on("click", "#remove_bill", function () {
                $(this).parent("div").remove();
            });
        });
    </script>
 
    <div id="bills">
        <input type="hidden" name="ex_id[]" value="{{ id }}">
        <input type="hidden" name="expense[]" value="expense">
        <input type="text" name="ex_type[]" id="ex_type" placeholder="Bill Name" />
        <input type="text" name="ex_amount[]" id="ex_amount" placeholder="Estimated Total" />
        <input type="date" name="ex_date[]" id="ex_date" placeholder="Payment Due" />
        <input type="button" id="add_bill" value="Add More" />
    </div>
 
    <input type="submit" name="submit" value="Submit" />
</form>
 
{% endblock %}
