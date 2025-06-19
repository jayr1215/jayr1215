class AppointmentService:
    PURPOSE_COSTS = {
        'Prophylaxis': 1500.00,
        'Dental Fillings': 2000.00,
        'Removable Dentures': 15000.00,
        'Tooth Extractions': 1000.00,
        'Dental Checkups & Diagnosis': 500.00,
        'Crowns & Bridges': 25000.00,
        'Orthodontics': 30000.00
    }

    @staticmethod
    def calculate_cost(purpose):
        return AppointmentService.PURPOSE_COSTS.get(purpose, 0.00)

    @staticmethod
    def process_payment(appointment, payment_method):
        # This is a placeholder for actual payment processing logic
        # In a real application, this would integrate with a payment gateway
        print(f"Processing {payment_method} payment for appointment {appointment.id} with cost {appointment.cost}")
        # Assuming payment is always successful for now
        return True