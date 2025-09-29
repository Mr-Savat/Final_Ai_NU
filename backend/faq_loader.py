import csv
import os

def load_faq(file_path):
    faqs = []
    
    # Check if file exists
    if not os.path.exists(file_path):
        print(f"FAQ file not found: {file_path}")
        # Create some default FAQs
        faqs = [
            {"question": "tuition fee", "answer": "For detailed tuition information, please contact the admissions office at Norton University."},
            {"question": "admission", "answer": "Admission requirements vary by program. Please visit our website or contact admissions."},
            {"question": "scholarship", "answer": "Norton University offers various scholarships. Check with the financial aid office for details."},
            {"question": "contact", "answer": "You can contact Norton University at: Phone: 023 999 999, Email: info@norton.edu.kh"}
        ]
        return faqs
    
    try:
        with open(file_path, mode='r', encoding='utf-8') as file:
            reader = csv.DictReader(file)
            for row in reader:
                faqs.append({
                    "question": row.get("question", "").strip(),
                    "answer": row.get("answer", "").strip()
                })
        print(f"Loaded {len(faqs)} FAQs from {file_path}")
    except Exception as e:
        print(f"Error loading FAQs: {e}")
    
    return faqs

def find_answer(user_question, faqs):
    if not faqs:
        return None
        
    user_question_lower = user_question.lower()
    
    # Simple keyword matching
    for faq in faqs:
        if faq["question"].lower() in user_question_lower:
            return faq["answer"]
    
    # Additional keyword matching for common questions
    keywords_mapping = {
        "tuition": "For tuition fees, please contact our admissions office.",
        "fee": "For fee information, please contact our admissions office.",
        "admission": "Admission requirements vary by program. Please visit our website.",
        "scholarship": "Scholarship information is available from the financial aid office.",
        "contact": "Contact Norton University at: Phone: 023 999 999, Email: info@norton.edu.kh",
        "location": "Norton University is located in Phnom Penh, Cambodia.",
        "deadline": "Application deadlines vary by program. Please check our website."
    }
    
    for keyword, answer in keywords_mapping.items():
        if keyword in user_question_lower:
            return answer
            
    return None