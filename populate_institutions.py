import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'adabiyya_smart_connect.settings')
django.setup()

from core.models import Institution

institutions_list = [
    "ആദബിയ ദഅ്വ കോളേജ്",
    "ശരീഅത്ത് സ്റ്റഡീസ് ഡിപ്പാർട്ട്മെന്റ്",
    "അറബിക് ലാംഗ്വേജ് അക്കാദമി",
    "ഇംഗ്ലീഷ് ആൻഡ് മോഡേൺ സയൻസ് ബ്ലോക്ക്",
    "ആദബിയ ഐടി & കമ്പ്യൂട്ടർ സെന്റർ",
    "ഹിഫ്ളുൽ ഖുർആൻ അക്കാദമി",
    "ആദബിയ പബ്ലിക് സ്കൂൾ",
    "പ്രീ-സ്കൂൾ ആൻഡ് നഴ്സറി",
    "വൊക്കേഷണൽ ട്രെയിനിംഗ് ഇൻസ്റ്റിറ്റ്യൂട്ട്",
    "ടീച്ചർ ട്രെയിനിംഗ് ഇൻസ്റ്റിറ്റ്യൂട്ട്",
    "ആദബിയ ഓർഫനേജ്",
    "ചാരിറ്റബിൾ ക്ലിനിക്",
    "റിലീഫ് സെന്റർ & കൗൺസിലിംഗ് യൂണിറ്റ്",
    "ബോയ്സ് ഹോസ്റ്റൽ",
    "ഗേൾസ് ഹോസ്റ്റൽ",
    "സ്റ്റാഫ് ക്വാർട്ടേഴ്സ്",
    "ആദബിയ സെൻട്രൽ ലൈബ്രറി",
    "സയൻസ് ലബോറട്ടറി",
    "മൾട്ടിമീഡിയ ആൻഡ് സ്മാർട്ട് ക്ലാസ്റൂം",
    "ഓഡിറ്റോറിയം ആൻഡ് പ്രാർത്ഥന ഹാൾ",
    "സ്പോർട്സ് ആൻഡ് ഫിറ്റ്നസ് ക്ലബ്",
    "പബ്ലിഷിംഗ് ആൻഡ് മീഡിയ വിംഗ്",
    "റിസർച്ച് സെന്റർ",
    "കരിയർ ഗൈഡൻസ് സെൽ",
    "അലുമിനി അസോസിയേഷൻ ഓഫീസ്",
    "മെസ് ഹാൾ ആൻഡ് കഫറ്റീരിയ",
    "അഡ്മിനിസ്ട്രേറ്റീവ് ബ്ലോക്ക്",
    "ഗസ്റ്റ് ഹൗസ്",
    "സ്കിൽ ഡെവലപ്മെന്റ് ലാബ്",
    "ഇലക്ട്രോണിക്സ് ആൻഡ് റോബോട്ടിക്സ് ലാബ്",
    "കർഷക സേവന കേന്ദ്രം",
    "ആദബിയ ട്രസ്റ്റ് ഓഫീസ്",
    "സോഷ്യൽ വെൽഫെയർ വിംഗ്"
]

def populate():
    print(f"Creating {len(institutions_list)} institutions...")
    
    # Optional: Clear existing to avoid duplicates if re-running
    # Institution.objects.all().delete() 
    
    for idx, name in enumerate(institutions_list, 1):
        code = f"INST_{idx:03d}"
        inst, created = Institution.objects.get_or_create(
            name=name,
            defaults={'code': code}
        )
        if created:
            print(f"Created: {name} ({code})")
        else:
            print(f"Exists: {name}")

if __name__ == '__main__':
    populate()
