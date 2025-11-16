"""
Payment Gateway Integration (Zarinpal)
"""
import requests
import json
from typing import Optional, Dict
from config import ZARINPAL_MERCHANT_ID, ZARINPAL_SANDBOX, ZARINPAL_CALLBACK_URL


class ZarinpalGateway:
    """Zarinpal Payment Gateway Integration"""
    
    SANDBOX_URL = "https://sandbox.zarinpal.com/pg/v4/payment/request.json"
    PRODUCTION_URL = "https://api.zarinpal.com/pg/v4/payment/request.json"
    
    SANDBOX_VERIFY_URL = "https://sandbox.zarinpal.com/pg/v4/payment/verify.json"
    PRODUCTION_VERIFY_URL = "https://api.zarinpal.com/pg/v4/payment/verify.json"
    
    def __init__(self):
        self.merchant_id = ZARINPAL_MERCHANT_ID
        self.sandbox = ZARINPAL_SANDBOX
        self.callback_url = ZARINPAL_CALLBACK_URL
        
    def get_base_url(self) -> str:
        """Get base URL for payment request"""
        return self.SANDBOX_URL if self.sandbox else self.PRODUCTION_URL
    
    def get_verify_url(self) -> str:
        """Get verify URL"""
        return self.SANDBOX_VERIFY_URL if self.sandbox else self.PRODUCTION_VERIFY_URL
    
    def create_payment_request(self, amount: int, description: str, 
                              metadata: Optional[Dict] = None) -> Dict:
        """
        Create payment request
        Returns: {'success': bool, 'authority': str, 'payment_url': str, 'message': str}
        """
        url = self.get_base_url()
        
        data = {
            "merchant_id": self.merchant_id,
            "amount": amount,
            "description": description,
            "callback_url": self.callback_url,
            "metadata": metadata or {}
        }
        
        try:
            response = requests.post(url, json=data, timeout=10)
            result = response.json()
            
            if result.get("data", {}).get("code") == 100:
                authority = result["data"]["authority"]
                payment_url = f"https://{'sandbox.' if self.sandbox else ''}zarinpal.com/pg/StartPay/{authority}"
                
                return {
                    'success': True,
                    'authority': authority,
                    'payment_url': payment_url,
                    'message': 'Payment request created successfully'
                }
            else:
                return {
                    'success': False,
                    'authority': None,
                    'payment_url': None,
                    'message': result.get("errors", {}).get("message", "Unknown error")
                }
        except Exception as e:
            return {
                'success': False,
                'authority': None,
                'payment_url': None,
                'message': str(e)
            }
    
    def verify_payment(self, authority: str, amount: int) -> Dict:
        """
        Verify payment
        Returns: {'success': bool, 'ref_id': str, 'message': str}
        """
        url = self.get_verify_url()
        
        data = {
            "merchant_id": self.merchant_id,
            "amount": amount,
            "authority": authority
        }
        
        try:
            response = requests.post(url, json=data, timeout=10)
            result = response.json()
            
            if result.get("data", {}).get("code") == 100:
                ref_id = result["data"]["ref_id"]
                return {
                    'success': True,
                    'ref_id': str(ref_id),
                    'message': 'Payment verified successfully'
                }
            elif result.get("data", {}).get("code") == 101:
                return {
                    'success': False,
                    'ref_id': None,
                    'message': 'Payment already verified'
                }
            else:
                return {
                    'success': False,
                    'ref_id': None,
                    'message': result.get("errors", {}).get("message", "Verification failed")
                }
        except Exception as e:
            return {
                'success': False,
                'ref_id': None,
                'message': str(e)
            }


# Global instance
payment_gateway = ZarinpalGateway()

