import qrcode
import io
import base64
from uuid import uuid4
import random
import string
from datetime import datetime

class QRCodeGenerator:
    """Generate QR codes for orders"""
    
    @staticmethod
    def generate_qr(order_id, order_token):
        """Generate QR code for order"""
        try:
            # Create QR data
            qr_data = f"QUICKBITE_ORDER:{order_id}|TOKEN:{order_token}"
            
            # Generate QR code
            qr = qrcode.QRCode(
                version=1,
                error_correction=qrcode.constants.ERROR_CORRECT_L,
                box_size=10,
                border=4,
            )
            qr.add_data(qr_data)
            qr.make(fit=True)
            
            img = qr.make_image(fill_color="black", back_color="white")
            
            # Convert to base64
            buffer = io.BytesIO()
            img.save(buffer, format='PNG')
            img_str = base64.b64encode(buffer.getvalue()).decode()
            
            return {
                'success': True,
                'qr_code': f'data:image/png;base64,{img_str}',
                'qr_data': qr_data
            }
        except Exception as e:
            return {
                'success': False,
                'error': str(e)
            }

class TokenGenerator:
    """Generate tokens for orders"""
    
    @staticmethod
    def generate_order_token():
        """Generate unique order token"""
        return ''.join(random.choices(string.ascii_uppercase + string.digits, k=6))
    
    @staticmethod
    def generate_unique_id():
        """Generate unique ID"""
        return str(uuid4())

class TimeScheduler:
    """Handle pickup time scheduling"""
    
    DELIVERY_SLOTS = [
        "12:00 PM",
        "12:30 PM",
        "1:00 PM",
        "1:30 PM",
        "2:00 PM",
        "2:30 PM",
        "3:00 PM",
        "5:00 PM",
        "5:30 PM",
        "6:00 PM",
        "6:30 PM",
        "7:00 PM",
    ]
    
    @staticmethod
    def get_available_slots():
        """Get available pickup slots"""
        return TimeScheduler.DELIVERY_SLOTS
    
    @staticmethod
    def validate_slot(slot):
        """Validate if slot is available"""
        return slot in TimeScheduler.DELIVERY_SLOTS
