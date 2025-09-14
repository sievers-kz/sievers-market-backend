class ConsoleEmailSender:
    async def send_confirmation_email(self, to: str, code: str):
        print("="*20, " MOCK EMAIL ", "="*20)
        print(f"TO: {to}")
        print(f"CODE: {code}")
        print("="*54)
