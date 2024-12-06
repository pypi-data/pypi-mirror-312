from datetime import datetime

class IdProperties:
    
    def id_generator(self, product_id, user_email):
        
        today = datetime.now().strftime("%Y%m%d")
        
        user_name = user_email.split('@')[0]
        
        contract_id = f"{today}-{product_id}-{user_name}"
        
        return contract_id
        