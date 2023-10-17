from flask import Flask, redirect, render_template, request, send_file, url_for
from fpdf import FPDF
import os
import random

app = Flask(__name__)

# Set your MySQL configurations
app.config['MYSQL_HOST'] = 'your_mysql_host'
app.config['MYSQL_USER'] = 'your_mysql_user'
app.config['MYSQL_PASSWORD'] = 'your_mysql_password'
app.config['MYSQL_DB'] = 'your_database_name'

# Remove duplicate function definition
def load_explanations(file_path):
    absolute_path = os.path.abspath(file_path)
    with open(absolute_path, 'r') as file:
        content = file.read()

    explanations = content.split('----')
    return random.choice(explanations)

@app.route('/')
def home():
    return render_template('index.html')

# Add other routes as needed
@app.route('/User')
def User():
    # return redirect(url_for('get_started'))
    return render_template('userInterface.html')

@app.route('/get_started')
def get_started():
    return render_template('GetStarted.html')

@app.route('/Lawyer')
def Lawyer():
    return render_template('lawyerInterface.html')

@app.route('/chat_bot_support')
def chat_bot_support():
    return render_template('chat-bot.html')

@app.route('/redirect_to_page3')
def redirect_to_page3():
    return redirect(url_for('user_sel'))


# Remove duplicate function definition
@app.route('/user_sel')
def user_sel():
    return render_template('form.html')

@app.route('/generate', methods=['POST'])
def generate():
    partner_data = []
    for i in range(1, 5):
        partner = {
            'Name': request.form[f'partner_{i}_name'],
            'Gender': request.form[f'partner_{i}_gender'],
            'Address Line 1': request.form[f'partner_{i}_address_1'],
            'Address Line 2': request.form[f'partner_{i}_address_2'],
            'City': request.form[f'partner_{i}_city'],
            'State': request.form[f'partner_{i}_state'],
            'Pin Code': request.form[f'partner_{i}_pin'],
        }
        partner_data.append(partner)

    partnership_details = {
        'Date': request.form['partnership_date'],
        'Business Activity': request.form['business_activity'],
        'Principal Place': request.form['principal_place'],
        'Duration': request.form['partnership_duration'],
        'Capital': request.form['initial_capital'],
    }

    witness_data = []
    for i in range(1, 3):
        witness = {
            'Name': request.form[f'witness_{i}_name'],
            'Address Line 1': request.form[f'witness_{i}_address_1'],
            'Address Line 2': request.form[f'witness_{i}_address_2'],
            'City': request.form[f'witness_{i}_city'],
            'State': request.form[f'witness_{i}_state'],
            'Pin Code': request.form[f'witness_{i}_pin'],
        }
        witness_data.append(witness)

    random_explanation = load_explanations('explainations.txt')

    deed_content = generate_deed_of_partnership(partner_data, partnership_details, witness_data, random_explanation)
    return render_template('preview.html', content=deed_content)

def generate_deed_of_partnership(partners, partnership_details, witnesses, random_explanation):
    pdf = PDF()
    pdf.add_page()

    deed_of_partnership = f"""
    Deed of Partnership

    This deed of partnership is made on {partnership_details['Date']} between:
    1. {partners[0]['Name']}, {partners[0]['Gender']} of {partners[0]['Address Line 1']}, residing at {partners[0]['Address Line 2']}, {partners[0]['City']}, {partners[0]['State']}, {partners[0]['Pin Code']} hereinafter referred to as FIRST PARTNER. \n
    2. {partners[1]['Name']}, {partners[1]['Gender']} of {partners[1]['Address Line 1']}, residing at {partners[1]['Address Line 2']}, {partners[1]['City']}, {partners[1]['State']}, {partners[1]['Pin Code']} hereinafter referred to as SECOND PARTNER. \n
    3. {partners[2]['Name']}, {partners[2]['Gender']} of {partners[2]['Address Line 1']}, residing at {partners[2]['Address Line 2']}, {partners[2]['City']}, {partners[2]['State']}, {partners[2]['Pin Code']} hereinafter referred to as THIRD PARTNER. \n
    4. {partners[3]['Name']}, {partners[3]['Gender']} of {partners[3]['Address Line 1']}, residing at {partners[3]['Address Line 2']}, {partners[3]['City']}, {partners[3]['State']}, {partners[3]['Pin Code']} hereinafter referred to as FOURTH PARTNER. \n

    Whereas, the parties hereto have agreed to commence business in partnership and it is expedient to have a written instrument of partnership. Now, this partnership deed witnesses as follows:

    1. BUSINESS ACTIVITY
    The parties hereto have mutually agreed to carry on the business of {partnership_details['Business Activity']}.

    2. PLACE OF BUSINESS
    The principal place of the partnership business will be situated at {partnership_details['Principal Place']}

    3. DURATION OF PARTNERSHIP
    The duration of the partnership will be {partnership_details['Duration']}.

    4. CAPITAL OF THE FIRM
    Initially, the capital of the firm shall be Rs. {partnership_details['Capital']}.

    5. PROFIT SHARING RATIO
    The profit or loss of the firm shall be shared equally among all the partners and transferred to the partners' current accounts.

    6. MANAGEMENT
    The {partners[0]['Name']} of the firm shall be the Managing Partner, and he will look after all the day-to-day transactions of the firm and any legal activities in the name of the firm, and the remaining partners shall cooperate to do so.

    7. OPERATION OF BANK ACCOUNTS
    The firm shall open a current account in the name of [Partnership Firm Name] at any bank, and such an account shall be operated by {partners[0]['Name']} and {partners[1]['Name']} jointly as declared from time to time to the Banks.

    8. BORROWING
    The written consent of all Partners will be required for the partnership to avail credit facilities from any financial institution.

    9. ACCOUNTS
    The firms shall regularly maintain, in the ordinary course of business, true and correct accounts of all its transactions and also of all its assets and liabilities, the property books of accounts, which shall ordinarily be kept at the firm’s place of business. The accounting year shall be the financial year from 1st April onwards, and the balance sheet shall be properly audited, and the same shall be signed by all the Partners. Every Partner shall have access to the books and the right to verify their correctness.

    10. RETIREMENT
    If any partner shall at any time during the subsistence of the partnership, be desirous of retiring from the firm, it shall be competent for him to do so, provided he shall give at least one calendar month notice of his intention of doing so. The remaining partners shall pay to the retiring partner or his legal representatives of the deceased partner, the purchase money of his share in the assets of the firm.

    11. DEATH OF PARTNER
    In the event of the death of any partners, one of the legal representatives of the deceased partner shall become the partner of the firm, and in the event the legal representatives show their denial to join the firm, they shall be paid the part of the purchase amount calculated as on the date of the death of the partner.

    12. ARBITRATION
    Whenever there be any difference of opinion or any dispute between the partners, the partners shall refer the same to an arbitration of one person. The decision of the arbitration so nominated shall be final and binding on all partners, such arbitration proceedings shall be governed by the Indian Arbitration Act, which is in force.

    In witness whereof, this deed of partnership is signed, sealed, and delivered this {partnership_details['Date']} at {witnesses[0]['City']}, {witnesses[0]['State']}:

    FIRST PARTNER

    {partners[0]['Address Line 1']}\t 
    {partners[0]['Address Line 2']}\t 
    {partners[0]['City']}, {partners[0]['State']}, {partners[0]['Pin Code']}\t

    SECOND PARTNER
    {partners[1]['Address Line 1']}
    {partners[1]['Address Line 2']}
    {partners[1]['City']}, {partners[1]['State']}, {partners[1]['Pin Code']}

    THIRD PARTNER
    {partners[2]['Address Line 1']}\t
    {partners[2]['Address Line 2']}\t
    {partners[2]['City']}, {partners[2]['State']}, {partners[2]['Pin Code']}\t

    FOURTH PARTNER
    {partners[3]['Address Line 1']}
    {partners[3]['Address Line 2']}
    {partners[3]['City']}, {partners[3]['State']}, {partners[3]['Pin Code']}

    WITNESS ONE
    {witnesses[0]['Address Line 1']}\t
    {witnesses[0]['Address Line 2']}\t
    {witnesses[0]['City']}, {witnesses[0]['State']}, {witnesses[0]['Pin Code']}\t

    WITNESS TWO
    {witnesses[1]['Address Line 1']}
    {witnesses[1]['Address Line 2']}
    {witnesses[1]['City']}, {witnesses[1]['State']}, {witnesses[1]['Pin Code']}
    """

    return pdf, deed_of_partnership

class PDF(FPDF):
    def __init__(self):
        super().__init__(orientation='P', unit='mm', format='legal')
        self.background_added = False

    def header(self):
        if not self.background_added:
            try:
                self.image('background.jpg', x=0, y=0, w=self.w, h=self.h)
                self.background_added = True
            except Exception as e:
                print(f"Error adding background image: {e}")
        self.set_font("Arial", "B", 12)
        self.cell(0, 10, " ", align="C", ln=True)

    def footer(self):
        self.set_y(-15)
        self.set_font("Arial", "I", 8)
        self.cell(0, 10, f"Page {self.page_no()}", 0, 0, "C")

    def chapter_title(self, title):
        if self.page_no() > 1:
            self.add_page()
        self.set_font("Arial", "B", 12)
        self.cell(0, 10, title, 0, 1)

    def chapter_body(self, body):
        self.set_y(self.h / 2)
        self.set_font("Arial", "", 12)
        self.multi_cell(0, 10, body.encode('latin-1', 'replace').decode('latin-1'))
        self.ln()

def save_pdf(content, filename):
    pdf, body_text = content
    pdf.chapter_title(" ")
    modified_body_text = body_text.replace('\u2019', "'")
    pdf.chapter_body(modified_body_text)
    pdf.output(filename)

def generate_pdf_content(filename):
    with open(filename, 'rb') as file:
        content = file.read()
    return content

# Add other routes as needed
@app.route('/Create_porfile')
def Create_porfile():
    return render_template('create.html')

@app.route('/Client')
def Client():
    return render_template('client.html')

@app.route('/Status')
def Status():
    return render_template('Status.html')

@app.route('/Updates')
def Updates():
    return render_template('Updates.html')

@app.route('/preview', methods=['POST'])
def preview():
    deed_content = generate_deed_of_partnership(partner_data, partnership_details, witness_data)
    return render_template('preview.html', content=deed_content)

@app.route('/download/<filename>')
def download(filename):
    pdf_filename = os.path.join(app.root_path, 'python', filename)
    return send_file(pdf_filename, as_attachment=True)


if __name__ == '__main__':
    app.run(debug=True)
