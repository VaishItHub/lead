from django.shortcuts import render

# Create your views here.
import pandas as pd
import pywhatkit as kit
import time
from django.shortcuts import render
from .forms import ExcelFileForm

def send_messages(request):
    if request.method == 'POST' and request.FILES['excel_file']:
        # Handle the uploaded file
        excel_file = request.FILES['excel_file']
        
        try:
            # Read the Excel file using pandas
            data = pd.read_excel(excel_file)
            
            # Loop through each contact in the file
            for index, row in data.iterrows():
                number = str(row['Number'])  # Ensure the number is a string
                message = row['Message']
                
                try:
                    # Send WhatsApp message
                    print(f"Sending message to {number}...")
                    kit.sendwhatmsg_instantly(f"+{number}", message)
                    
                    # Wait to avoid being flagged as spam
                    time.sleep(10)
                except Exception as e:
                    print(f"Failed to send message to {number}. Error: {e}")
            
            return render(request, 'contacts/message_sent.html', {'message': 'All messages sent successfully!'})
        except Exception as e:
            return render(request, 'contacts/message_sent.html', {'message': f"Error: {e}"})
    
    # Render form if not a POST request
    form = ExcelFileForm()
    return render(request, 'contacts/upload_file.html', {'form': form})
