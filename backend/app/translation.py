from deep_translator import GoogleTranslator
import logging

logger = logging.getLogger(__name__)

class TranslationService:
    def __init__(self):
        self.supported_languages = {
            'en': 'English',
            'hi': 'Hindi', 
            'kn': 'Kannada',
            'te': 'Telugu',
            'ta': 'Tamil',
            'mr': 'Marathi',
            'bn': 'Bengali',
            'gu': 'Gujarati',
            'ml': 'Malayalam',
            'pa': 'Punjabi'
        }
        
        # ULTRA-COMPREHENSIVE keyword mapping - ALL STATES & DISTRICTS IN ALL LANGUAGES
        self.keyword_map = {
            
            # ==================== KARNATAKA DISTRICTS (ALL LANGUAGES) ====================
            # Bangalore / Bengaluru
            'ಬೆಂಗಳೂರು': 'bangalore', 'बेंगलुरु': 'bangalore', 'பெங்களூரு': 'bangalore',
            'బెంగళూరు': 'bangalore', 'ബെംഗളൂരു': 'bangalore', 'बेंगलुरू': 'bangalore',
            'বেঙ্গালুরু': 'bangalore', 'બેંગલોર': 'bangalore', 'ਬੰਗਲੌਰ': 'bangalore',
            'bengaluru': 'bangalore', 'bangaluru': 'bangalore',
            
            # Mysore / Mysuru
            'ಮೈಸೂರು': 'mysore', 'मैसूर': 'mysore', 'மைசூர்': 'mysore',
            'మైసూరు': 'mysore', 'മൈസൂര്': 'mysore', 'मैसूर': 'mysore',
            'ময়সুর': 'mysore', 'મૈસૂર': 'mysore', 'ਮੈਸੂਰ': 'mysore',
            'mysuru': 'mysore', 'maisuru': 'mysore',
            
            # Hubli / Hubballi
            'ಹುಬ್ಬಳ್ಳಿ': 'hubli', 'हुबली': 'hubli', 'ஹூபளி': 'hubli',
            'హుబ్లీ': 'hubli', 'ഹബ്ലി': 'hubli', 'हुबळी': 'hubli',
            'হুবলি': 'hubli', 'હુબલી': 'hubli', 'ਹੁਬਲੀ': 'hubli',
            'hubballi': 'hubli', 'dharwad hubli': 'hubli',
            
            # Mangalore / Mangaluru
            'ಮಂಗಳೂರು': 'mangalore', 'मैंगलोर': 'mangalore', 'மங்களூர்': 'mangalore',
            'మంగళూరు': 'mangalore', 'മംഗലൂര്': 'mangalore', 'मंगळूर': 'mangalore',
            'মাঙ্গালোর': 'mangalore', 'મંગલોર': 'mangalore', 'ਮੰਗਲੌਰ': 'mangalore',
            'mangaluru': 'mangalore', 'mangaloor': 'mangalore',
            
            # Belgaum / Belagavi
            'ಬೆಳಗಾವಿ': 'belgaum', 'बेलगाम': 'belgaum', 'பெலகாம்': 'belgaum',
            'బెలగావి': 'belgaum', 'ബെലഗാവി': 'belgaum', 'बेळगांव': 'belgaum',
            'বেলগাঁও': 'belgaum', 'બેલગામ': 'belgaum', 'ਬੇਲਗਾਂਵ': 'belgaum',
            'belagavi': 'belgaum', 'belgavi': 'belgaum',
            
            # Gulbarga / Kalaburagi
            'ಕಲಬುರಗಿ': 'gulbarga', 'गुलबर्गा': 'gulbarga', 'குல்பர்கா': 'gulbarga',
            'గుల్బర్గా': 'gulbarga', 'ഗുൽബർഗ': 'gulbarga', 'गुलबर्गा': 'gulbarga',
            'গুলবর্গা': 'gulbarga', 'ગુલબર્ગા': 'gulbarga', 'ਗੁਲਬਰਗਾ': 'gulbarga',
            'kalaburagi': 'gulbarga', 'kalburgi': 'gulbarga',
            
            # Davangere
            'ದಾವಣಗೆರೆ': 'davangere', 'दावणगेरे': 'davangere', 'தாவங்கெரே': 'davangere',
            'దావణగెరే': 'davangere', 'ദാവങ്ങെരെ': 'davangere', 'दावणगेरे': 'davangere',
            'দাবনগিরি': 'davangere', 'દાવણગેરે': 'davangere', 'ਦਾਵਣਗੇਰੇ': 'davangere',
            
            # Ballari / Bellary
            'ಬಲ್ಲಾರಿ': 'bellary', 'बल्लारी': 'bellary', 'பல்லாரி': 'bellary',
            'బల్లారి': 'bellary', 'ബല്ലാരി': 'bellary', 'बल्लारी': 'bellary',
            'বেল্লারি': 'bellary', 'બલ્લારી': 'bellary', 'ਬੱਲਾਰੀ': 'bellary',
            'ballari': 'bellary', 'belari': 'bellary',
            
            # Bijapur / Vijayapura
            'ಬೀಜಾಪುರ': 'bijapur', 'बीजापुर': 'bijapur', 'பீஜாபூர்': 'bijapur',
            'బిజాపూర్': 'bijapur', 'ബീജാപൂര്': 'bijapur', 'बीजापूर': 'bijapur',
            'বিজাপুর': 'bijapur', 'બીજાપુર': 'bijapur', 'ਬੀਜਾਪੁਰ': 'bijapur',
            'vijayapura': 'bijapur', 'vijayapur': 'bijapur',
            
            # Shimoga / Shivamogga
            'ಶಿವಮೊಗ್ಗ': 'shimoga', 'शिवमोग्गा': 'shimoga', 'சிவமொக்கா': 'shimoga',
            'శివమొగ్గ': 'shimoga', 'ശിവമോഗ്ഗ': 'shimoga', 'शिवमोग्गा': 'shimoga',
            'শিবমোগা': 'shimoga', 'શિવમોગા': 'shimoga', 'ਸ਼ਿਵਮੋਗਾ': 'shimoga',
            'shimogga': 'shimoga', 'shivamogga': 'shimoga',
            
            # Tumkur / Tumakuru
            'ತುಮಕೂರು': 'tumkur', 'तुमकुरु': 'tumkur', 'துமகூரு': 'tumkur',
            'తుమకూరు': 'tumkur', 'തുമകൂരു': 'tumkur', 'तुमकुरू': 'tumkur',
            'তুমকুর': 'tumkur', 'તુમકુર': 'tumkur', 'ਤੁਮਕੁਰ': 'tumkur',
            'tumakuru': 'tumkur', 'tumkoor': 'tumkur',
            
            # Raichur
            'ರಾಯಚೂರು': 'raichur', 'रायचूर': 'raichur', 'ராய்சூர்': 'raichur',
            'రాయచూరు': 'raichur', 'റായ്ചൂര്': 'raichur', 'रायचूर': 'raichur',
            'রায়চুর': 'raichur', 'રાયચુર': 'raichur', 'ਰਾਇਚੁਰ': 'raichur',
            
            # Bidar
            'ಬೀದರ್': 'bidar', 'बीदर': 'bidar', 'பீதர்': 'bidar',
            'బీదర్': 'bidar', 'ബീദർ': 'bidar', 'बीदर': 'bidar',
            'বিদার': 'bidar', 'બીદર': 'bidar', 'ਬੀਦਰ': 'bidar',
            
            # Hassan
            'ಹಾಸನ': 'hassan', 'हासन': 'hassan', 'ஹாசன்': 'hassan',
            'హాసన్': 'hassan', 'ഹാസന്': 'hassan', 'हासन': 'hassan',
            'হাসান': 'hassan', 'હાસન': 'hassan', 'ਹਾਸਨ': 'hassan',
            
            # Gadag
            'ಗದಗ': 'gadag', 'गदग': 'gadag', 'கதக்': 'gadag',
            'గదగ్': 'gadag', 'ഗദഗ്': 'gadag', 'गदग': 'gadag',
            'গদগ': 'gadag', 'ગદગ': 'gadag', 'ਗਦਗ': 'gadag',
            
            # Mandya
            'ಮಾಂಡ್ಯ': 'mandya', 'मांड्या': 'mandya', 'மாண்ட்யா': 'mandya',
            'మాండ్యా': 'mandya', 'മാണ്ഡ്യ': 'mandya', 'मांड्या': 'mandya',
            'মান্ড্যা': 'mandya', 'માંડ્યા': 'mandya', 'ਮਾਂਡਿਆ': 'mandya',
            
            # Udupi
            'ಉಡುಪಿ': 'udupi', 'उडुपी': 'udupi', 'உடுப்பி': 'udupi',
            'ఉడుపి': 'udupi', 'ഉഡുപി': 'udupi', 'उडुपी': 'udupi',
            'উদুপি': 'udupi', 'ઉડુપી': 'udupi', 'ਉਡੁਪੀ': 'udupi',
            
            # Chikmagalur / Chikkamagaluru
            'ಚಿಕ್ಕಮಗಳೂರು': 'chikmagalur', 'चिकमगलूर': 'chikmagalur', 'சிக்மகலூர்': 'chikmagalur',
            'చిక్మగళూరు': 'chikmagalur', 'ചിക്മഗളൂര്': 'chikmagalur', 'चिकमगलूर': 'chikmagalur',
            'চিকমাগালুর': 'chikmagalur', 'ચિકમગલુર': 'chikmagalur', 'ਚਿਕਮਾਗਲੂਰ': 'chikmagalur',
            'chikkamagaluru': 'chikmagalur', 'chickmagalur': 'chikmagalur',
            
            # Kodagu / Coorg
            'ಕೊಡಗು': 'kodagu', 'कोडागु': 'kodagu', 'கோடகு': 'kodagu',
            'కోడగు': 'kodagu', 'കോഡഗു': 'kodagu', 'कोडागु': 'kodagu',
            'কোদাগু': 'kodagu', 'કોડાગુ': 'kodagu', 'ਕੋਡਾਗੂ': 'kodagu',
            'coorg': 'kodagu',
            
            # Dharwad
            'ಧಾರವಾಡ': 'dharwad', 'धारवाड़': 'dharwad', 'தார்வாட்': 'dharwad',
            'ధార్వాడ్': 'dharwad', 'ധര്‍വാഡ്': 'dharwad', 'धारवाड': 'dharwad',
            'ধারওয়াড': 'dharwad', 'ધારવાડ': 'dharwad', 'ਧਾਰਵਾੜ': 'dharwad',
            'dharwar': 'dharwad',
            
            # Bagalkot
            'ಬಾಗಲಕೋಟೆ': 'bagalkot', 'बागलकोट': 'bagalkot', 'பாகல்கோட்': 'bagalkot',
            'బాగల్‌కోట్': 'bagalkot', 'ബാഗല്‍കോട്ട്': 'bagalkot', 'बागलकोट': 'bagalkot',
            'বাগালকোট': 'bagalkot', 'બાગલકોટ': 'bagalkot', 'ਬਾਗਲਕੋਟ': 'bagalkot',
            
            # Haveri
            'ಹಾವೇರಿ': 'haveri', 'हावेरी': 'haveri', 'ஹவேரி': 'haveri',
            'హావేరి': 'haveri', 'ഹവേരി': 'haveri', 'हावेरी': 'haveri',
            'হাভেরি': 'haveri', 'હવેરી': 'haveri', 'ਹਾਵੇਰੀ': 'haveri',
            
            # Chitradurga
            'ಚಿತ್ರದುರ್ಗ': 'chitradurga', 'चित्रदुर्गा': 'chitradurga', 'சித்திரதுர்கா': 'chitradurga',
            'చిత్రదుర్గ': 'chitradurga', 'ചിത്രദുര്‍ഗ': 'chitradurga', 'चित्रदुर्ग': 'chitradurga',
            'চিত্রদুর্গ': 'chitradurga', 'ચિત્રદુર્ગ': 'chitradurga', 'ਚਿਤਰਦੁਰਗ': 'chitradurga',
            
            # Koppal
            'ಕೊಪ್ಪಳ': 'koppal', 'कोप्पल': 'koppal', 'கொப்பல்': 'koppal',
            'కొప్పల్': 'koppal', 'കൊപ്പല്': 'koppal', 'कोप्पल': 'koppal',
            'কোপ্পাল': 'koppal', 'કોપ્પલ': 'koppal', 'ਕੋਪਾਲ': 'koppal',
            
            # Uttara Kannada
            'ಉತ್ತರ ಕನ್ನಡ': 'uttara kannada', 'उत्तर कन्नड़': 'uttara kannada', 'உத்தர கன்னட': 'uttara kannada',
            'ఉత్తర కన్నడ': 'uttara kannada', 'ഉത്തര കന്നഡ': 'uttara kannada',
            'karwar': 'uttara kannada', 'कारवार': 'uttara kannada',
            
            # Dakshina Kannada
            'ದಕ್ಷಿಣ ಕನ್ನಡ': 'dakshina kannada', 'दक्षिण कन्नड़': 'dakshina kannada',
            'தக்ஷிண கன்னட': 'dakshina kannada', 'దక్షిణ కన్నడ': 'dakshina kannada',
            
            # Chamarajanagar
            'ಚಾಮರಾಜನಗರ': 'chamarajanagar', 'चामराजनगर': 'chamarajanagar',
            'சாமராஜநகர்': 'chamarajanagar', 'చామరాజనగర్': 'chamarajanagar',
            
            # Chikkaballapur
            'ಚಿಕ್ಕಬಳ್ಳಾಪುರ': 'chikkaballapur', 'चिक्कबल्लापुर': 'chikkaballapur',
            
            # Kolar
            'ಕೋಲಾರ': 'kolar', 'कोलार': 'kolar', 'கோலார்': 'kolar',
            'కోలార్': 'kolar', 'കോലാര്': 'kolar',
            
            # Ramanagara
            'ರಾಮನಗರ': 'ramanagara', 'रामनगर': 'ramanagara', 'ராமநகர்': 'ramanagara',
            
            # Yadgir
            'ಯಾದಗಿರಿ': 'yadgir', 'यादगीर': 'yadgir', 'யாத்கீர்': 'yadgir',
            
            
            # ==================== MAHARASHTRA DISTRICTS ====================
            # Mumbai
            'मुंबई': 'mumbai', 'ముంబై': 'mumbai', 'மும்பை': 'mumbai',
            'ಮುಂಬೈ': 'mumbai', 'മുംബൈ': 'mumbai', 'মুম্বাই': 'mumbai',
            'મુંબઈ': 'mumbai', 'ਮੁੰਬਈ': 'mumbai', 'bombay': 'mumbai',
            
            # Pune
            'पुणे': 'pune', 'పూణే': 'pune', 'புணே': 'pune',
            'ಪುಣೆ': 'pune', 'പൂണേ': 'pune', 'পুনে': 'pune',
            'પૂણે': 'pune', 'ਪੁਣੇ': 'pune', 'poona': 'pune',
            
            # Nagpur
            'नागपुर': 'nagpur', 'నాగ్‌పూర్': 'nagpur', 'நாக்பூர்': 'nagpur',
            'ನಾಗಪುರ': 'nagpur', 'നാഗ്പൂര്': 'nagpur', 'নাগপুর': 'nagpur',
            'નાગપુર': 'nagpur', 'ਨਾਗਪੁਰ': 'nagpur',
            
            # Thane
            'ठाणे': 'thane', 'తానే': 'thane', 'தானே': 'thane',
            'ಠಾಣೆ': 'thane', 'ടാനെ': 'thane', 'ঠাণে': 'thane',
            
            # Nashik
            'नाशिक': 'nashik', 'నాసిక్': 'nashik', 'நாசிக்': 'nashik',
            'ನಾಶಿಕ್': 'nashik', 'നാസിക്': 'nashik',
            
            # Aurangabad
            'औरंगाबाद': 'aurangabad', 'ఔరంగాబాద్': 'aurangabad', 'ஔரங்காபாத்': 'aurangabad',
            'ಔರಂಗಾಬಾದ್': 'aurangabad', 'ഔരംഗാബാദ്': 'aurangabad',
            
            # Solapur
            'सोलापुर': 'solapur', 'సోలాపూర్': 'solapur', 'சோலாப்பூர்': 'solapur',
            
            # Kolhapur
            'कोल्हापुर': 'kolhapur', 'కోల్‌హాపూర్': 'kolhapur', 'கோல்ஹாப்பூர்': 'kolhapur',
            
            # Ahmednagar
            'अहमदनगर': 'ahmednagar', 'అహ్మద్‌నగర్': 'ahmednagar',
            
            # Satara
            'सातारा': 'satara', 'సతార': 'satara',
            
            # Sangli
            'सांगली': 'sangli', 'సాంగ్లీ': 'sangli',
            
            # Jalgaon
            'जळगांव': 'jalgaon', 'జల్గావ్': 'jalgaon',
            
            # Akola
            'अकोला': 'akola', 'అకోలా': 'akola',
            
            # Amravati
            'अमरावती': 'amravati', 'అమరావతి': 'amravati',
            
            # Ratnagiri
            'रत्नागिरी': 'ratnagiri', 'రత్నగిరి': 'ratnagiri',
            
            
            # ==================== TAMIL NADU DISTRICTS ====================
            # Chennai
            'சென்னை': 'chennai', 'चेन्नई': 'chennai', 'చెన్నై': 'chennai',
            'ಚೆನ್ನೈ': 'chennai', 'ചെന്നൈ': 'chennai', 'চেন্নাই': 'chennai',
            'ચેન્નઈ': 'chennai', 'ਚੇਨਈ': 'chennai', 'madras': 'chennai',
            
            # Coimbatore
            'கோயம்புத்தூர்': 'coimbatore', 'कोयम्बटूर': 'coimbatore', 'కోయంబత్తూరు': 'coimbatore',
            'ಕೋಯಮತ್ತೂರ': 'coimbatore', 'കോയമ്പത്തൂര്': 'coimbatore',
            
            # Madurai
            'மதுரை': 'madurai', 'मदुरै': 'madurai', 'మదురై': 'madurai',
            'ಮಧುರೈ': 'madurai', 'മദുര': 'madurai',
            
            # Tiruchirappalli / Trichy
            'திருச்சிராப்பள்ளி': 'trichy', 'तिरुचिरापल्ली': 'trichy', 'తిరుచ్చిరాప్పల్లి': 'trichy',
            'tiruchirappalli': 'trichy',
            
            # Salem
            'சேலம்': 'salem', 'सलेम': 'salem', 'సేలం': 'salem',
            'ಸೇಲಂ': 'salem', 'സേലം': 'salem',
            
            # Tirunelveli
            'திருநெல்வேலி': 'tirunelveli', 'तिरुनेलवेली': 'tirunelveli',
            
            # Tiruppur
            'திருப்பூர்': 'tiruppur', 'तिरुप्पूर': 'tiruppur',
            
            # Vellore
            'வேலூர்': 'vellore', 'वेल्लोर': 'vellore', 'వెల్లూరు': 'vellore',
            
            # Erode
            'ஈரோடு': 'erode', 'इरोड': 'erode',
            
            # Thanjavur
            'தஞ்சாவூர்': 'thanjavur', 'तंजावुर': 'thanjavur',
            
            # Kanyakumari
            'கன்னியாகுமரி': 'kanyakumari', 'कन्याकुमारी': 'kanyakumari',
            
            
            # ==================== ANDHRA PRADESH & TELANGANA DISTRICTS ====================
            # Hyderabad
            'హైదరాబాద్': 'hyderabad', 'हैदराबाद': 'hyderabad', 'ஹைதராபாத்': 'hyderabad',
            'ಹೈದರಾಬಾದ್': 'hyderabad', 'ഹൈദരാബാദ്': 'hyderabad', 'হায়দরাবাদ': 'hyderabad',
            'હૈદરાબાદ': 'hyderabad', 'ਹੈਦਰਾਬਾਦ': 'hyderabad',
            
            # Visakhapatnam
            'విశాఖపట్నం': 'visakhapatnam', 'विशाखापत्तनम': 'visakhapatnam', 'விசாகப்பட்டினம்': 'visakhapatnam',
            'ವಿಶಾಖಪಟ್ಟಣಂ': 'visakhapatnam', 'വിശാഖപട്ടണം': 'visakhapatnam',
            'vizag': 'visakhapatnam', 'vishakhapatnam': 'visakhapatnam',
            
            # Vijayawada
            'విజయవాడ': 'vijayawada', 'विजयवाड़ा': 'vijayawada', 'விஜயவாடா': 'vijayawada',
            'ವಿಜಯವಾಡ': 'vijayawada',
            
            # Guntur
            'గుంటూరు': 'guntur', 'गुंटूर': 'guntur', 'குந்தூர்': 'guntur',
            
            # Warangal
            'వరంగల్': 'warangal', 'वारंगल': 'warangal',
            
            # Nellore
            'నెల్లూరు': 'nellore', 'नेल्लूर': 'nellore',
            
            # Tirupati
            'తిరుపతి': 'tirupati', 'तिरुपति': 'tirupati', 'திருப்பதி': 'tirupati',
            
            # Karimnagar
            'కరీంనగర్': 'karimnagar', 'करीमनगर': 'karimnagar',
            
            
            # ==================== KERALA DISTRICTS ====================
            # Thiruvananthapuram / Trivandrum
            'തിരുവനന്തപുരം': 'thiruvananthapuram', 'तिरुवनंतपुरम': 'thiruvananthapuram',
            'திருவனந்தபுரம்': 'thiruvananthapuram', 'తిరువనంతపురం': 'thiruvananthapuram',
            'trivandrum': 'thiruvananthapuram',
            
            # Kochi / Cochin
            'കൊച്ചി': 'kochi', 'कोच्चि': 'kochi', 'கொச்சி': 'kochi',
            'కొచ్చి': 'kochi', 'ಕೊಚ್ಚಿ': 'kochi', 'cochin': 'kochi',
            
            # Kozhikode / Calicut
            'കോഴിക്കോട്': 'kozhikode', 'कोझिकोड': 'kozhikode', 'கோழிக்கோடு': 'kozhikode',
            'calicut': 'kozhikode',
            
            # Kollam
            'കൊല്ലം': 'kollam', 'कोल्लम': 'kollam', 'கொல்லம்': 'kollam',
            
            # Thrissur
            'തൃശ്ശൂര്': 'thrissur', 'त्रिशूर': 'thrissur',
            
            # Kannur
            'കണ്ണൂര്': 'kannur', 'कण्णूर': 'kannur',
            
            # Alappuzha
            'ആലപ്പുഴ': 'alappuzha', 'आलप्पुझा': 'alappuzha', 'alleppey': 'alappuzha',
            
            # Palakkad
            'പാലക്കാട്': 'palakkad', 'पालक्काड': 'palakkad',
            
            # Malappuram
            'മലപ്പുറം': 'malappuram', 'मलप्पुरम': 'malappuram',
            
            # Kottayam
            'കോട്ടയം': 'kottayam', 'कोट्टयम': 'kottayam',
            
            
            # ==================== GUJARAT DISTRICTS ====================
            # Ahmedabad
            'અમદાવાદ': 'ahmedabad', 'अहमदाबाद': 'ahmedabad', 'அகமதாபாத்': 'ahmedabad',
            'అహ్మదాబాద్': 'ahmedabad', 'അഹമ്മദാബാദ്': 'ahmedabad', 'আহমেদাবাদ': 'ahmedabad',
            'ਅਹਿਮਦਾਬਾਦ': 'ahmedabad', 'amdavad': 'ahmedabad',
            
            # Surat
            'સુરત': 'surat', 'सूरत': 'surat', 'சூரத்': 'surat',
            'సూరత్': 'surat', 'സൂററ്': 'surat',
            
            # Vadodara / Baroda
            'વડોદરા': 'vadodara', 'वडोदरा': 'vadodara', 'வடோதரா': 'vadodara',
            'baroda': 'vadodara',
            
            # Rajkot
            'રાજકોટ': 'rajkot', 'राजकोट': 'rajkot', 'ராஜ்கோட்': 'rajkot',
            
            # Bhavnagar
            'ભાવનગર': 'bhavnagar', 'भावनगर': 'bhavnagar',
            
            # Jamnagar
            'જામનગર': 'jamnagar', 'जामनगर': 'jamnagar',
            
            
            # ==================== WEST BENGAL DISTRICTS ====================
            # Kolkata / Calcutta
            'কলকাতা': 'kolkata', 'कोलकाता': 'kolkata', 'கொல்கத்தா': 'kolkata',
            'కోల్‌కతా': 'kolkata', 'കോൽക്കത്ത': 'kolkata', 'કોલકાતા': 'kolkata',
            'ਕੋਲਕਾਤਾ': 'kolkata', 'calcutta': 'kolkata',
            
            # Darjeeling
            'দার্জিলিং': 'darjeeling', 'दार्जीलिंग': 'darjeeling', 'தார்ஜிலிங்': 'darjeeling',
            
            # Howrah
            'হাওড়া': 'howrah', 'हावड़ा': 'howrah',
            
            # Siliguri
            'শিলিগুড়ি': 'siliguri', 'सिलीगुड़ी': 'siliguri',
            
            
            # ==================== PUNJAB DISTRICTS ====================
            # Ludhiana
            'ਲੁਧਿਆਣਾ': 'ludhiana', 'लुधियाना': 'ludhiana', 'லுதியானா': 'ludhiana',
            'లుధియానా': 'ludhiana', 'ലുധിയാന': 'ludhiana',
            
            # Amritsar
            'ਅੰਮ੍ਰਿਤਸਰ': 'amritsar', 'अमृतसर': 'amritsar', 'அம்ரித்சர்': 'amritsar',
            
            # Jalandhar
            'ਜਲੰਧਰ': 'jalandhar', 'जालंधर': 'jalandhar',
            
            # Patiala
            'ਪਟਿਆਲਾ': 'patiala', 'पटियाला': 'patiala',
            
            
            # ==================== RAJASTHAN DISTRICTS ====================
            # Jaipur
            'जयपुर': 'jaipur', 'ஜெய்ப்பூர்': 'jaipur', 'జైపూర్': 'jaipur',
            'ജയ്പൂര്': 'jaipur', 'জয়পুর': 'jaipur', 'જયપુર': 'jaipur',
            
            # Jodhpur
            'जोधपुर': 'jodhpur', 'ஜோத்பூர்': 'jodhpur',
            
            # Udaipur
            'उदयपुर': 'udaipur', 'உதய்ப்பூர்': 'udaipur',
            
            # Kota
            'कोटा': 'kota', 'கோட்டா': 'kota',
            
            
            # ==================== DELHI ====================
            # Delhi / New Delhi
            'दिल्ली': 'delhi', 'டெல்லி': 'delhi', 'ఢిల్లీ': 'delhi',
            'ഡൽഹി': 'delhi', 'দিল্লি': 'delhi', 'દિલ્લી': 'delhi',
            'ਦਿੱਲੀ': 'delhi', 'new delhi': 'delhi',
            
            
            # ==================== STATES (ALL LANGUAGES) ====================
            # Karnataka
            'ಕರ್ನಾಟಕ': 'karnataka', 'कर्नाटक': 'karnataka', 'கர்நாடகா': 'karnataka',
            'కర్ణాటక': 'karnataka', 'കര്‍ണാടക': 'karnataka', 'কর্ণাটক': 'karnataka',
            'કર્ણાટક': 'karnataka', 'ਕਰਨਾਟਕ': 'karnataka',
            
            # Maharashtra
            'महाराष्ट्र': 'maharashtra', 'மஹாராஷ்டிரா': 'maharashtra', 'మహారాష్ట్ర': 'maharashtra',
            'മഹാരാഷ്ട്ര': 'maharashtra', 'মহারাষ্ট্র': 'maharashtra', 'મહારાષ્ટ્ર': 'maharashtra',
            'ਮਹਾਰਾਸ਼ਟਰ': 'maharashtra',
            
            # Tamil Nadu
            'தமிழ்நாடு': 'tamil nadu', 'तमिल नाडु': 'tamil nadu', 'తమిళనాడు': 'tamil nadu',
            'തമിഴ്നാട്': 'tamil nadu', 'তামিলনাডু': 'tamil nadu', 'તમિલનાડુ': 'tamil nadu',
            'तमिलनाडु': 'tamil nadu', 'ತಮಿಳುನಾಡು': 'tamil nadu',
            
            # Kerala
            'കേരളം': 'kerala', 'केरल': 'kerala', 'கேரளா': 'kerala',
            'కేరళ': 'kerala', 'কেরল': 'kerala', 'કેરળ': 'kerala',
            'ਕੇਰਲ': 'kerala', 'ಕೇರಳ': 'kerala',
            
            # Andhra Pradesh
            'ఆంధ్ర ప్రదేశ్': 'andhra pradesh', 'आंध्र प्रदेश': 'andhra pradesh',
            'ஆந்திரப் பிரதேசம்': 'andhra pradesh', 'ആന്ധ്രപ്രദേശ്': 'andhra pradesh',
            
            # Telangana
            'తెలంగాణ': 'telangana', 'तेलंगाना': 'telangana', 'తెలంగాణ': 'telangana',
            
            # Gujarat
            'ગુજરાત': 'gujarat', 'गुजरात': 'gujarat', 'குஜராத்': 'gujarat',
            'గుజరాత్': 'gujarat', 'ഗുജറാത്ത്': 'gujarat', 'গুজরাট': 'gujarat',
            'ਗੁਜਰਾਤ': 'gujarat', 'ಗುಜರಾತ್': 'gujarat',
            
            # Punjab
            'ਪੰਜਾਬ': 'punjab', 'पंजाब': 'punjab', 'பஞ்சாப்': 'punjab',
            'పంజాబ్': 'punjab', 'പഞ്ചാബ്': 'punjab', 'পাঞ্জাব': 'punjab',
            'પંજાબ': 'punjab', 'ಪಂಜಾಬ್': 'punjab',
            
            # West Bengal
            'পশ্চিমবঙ্গ': 'west bengal', 'पश्चिम बंगाल': 'west bengal',
            'மேற்கு வங்காளம்': 'west bengal', 'పశ్చిమ బెంగాల్': 'west bengal',
            
            # Rajasthan
            'राजस्थान': 'rajasthan', 'ராஜஸ்தான்': 'rajasthan', 'రాజస్థాన్': 'rajasthan',
            'രാജസ്ഥാന്': 'rajasthan', 'রাজস্থান': 'rajasthan', 'રાજસ્થાન': 'rajasthan',
            
            # Uttar Pradesh
            'उत्तर प्रदेश': 'uttar pradesh', 'உத்தரப் பிரதேசம்': 'uttar pradesh',
            'ఉత్తర ప్రదేశ్': 'uttar pradesh', 'উত্তরপ্রদেশ': 'uttar pradesh',
            
            # Madhya Pradesh
            'मध्य प्रदेश': 'madhya pradesh', 'மத்தியப் பிரதேசம்': 'madhya pradesh',
            
            # Bihar
            'बिहार': 'bihar', 'பீகார்': 'bihar', 'బిహార్': 'bihar',
            'ബിഹാര്': 'bihar', 'বিহার': 'bihar',
            
            # Odisha
            'ଓଡ଼ିଶା': 'odisha', 'ओडिशा': 'odisha', 'ஒடிசா': 'odisha',
            
            # Assam
            'অসম': 'assam', 'असम': 'assam', 'அஸ்ஸாம்': 'assam',
            
            # Haryana
            'हरियाणा': 'haryana', 'ஹரியானா': 'haryana',
            
            # Jharkhand
            'झारखंड': 'jharkhand', 'ஜார்கண்ட்': 'jharkhand',
            
            # Chhattisgarh
            'छत्तीसगढ़': 'chhattisgarh', 'சத்தீஸ்கர்': 'chhattisgarh',
            
            # Uttarakhand
            'उत्तराखंड': 'uttarakhand', 'உத்தரகண்ட்': 'uttarakhand',
            
            # Himachal Pradesh
            'हिमाचल प्रदेश': 'himachal pradesh',
            
            # Jammu and Kashmir
            'जम्मू और कश्मीर': 'jammu and kashmir',
            
            # Goa
            'गोवा': 'goa', 'கோவா': 'goa', 'గోవా': 'goa',
            'ഗോവ': 'goa', 'গোয়া': 'goa', 'ગોવા': 'goa',
            
            
            # ==================== COMMON WORDS/ACTIONS (ALL LANGUAGES) ====================
            # Water
            'ನೀರಿನ': 'water', 'ನೀರು': 'water', 'पानी': 'water', 'நீர்': 'water',
            'నీరు': 'water', 'വെള്ളം': 'water', 'জল': 'water', 'પાણી': 'water',
            'ਪਾਣੀ': 'water', 'जल': 'water', 'தண்ணீர்': 'water',
            
            # Information / Data
            'ಮಾಹಿತಿ': 'information', 'माहिती': 'information', 'தகவல்': 'information',
            'సమాచారం': 'information', 'വിവരം': 'information', 'তথ্য': 'information',
            'માહિતી': 'information', 'ਜਾਣਕਾਰੀ': 'information', 'जानकारी': 'information',
            'ಡೇಟಾ': 'data', 'डेटा': 'data', 'தரவு': 'data', 'డేటా': 'data',
            
            # About
            'ಬಗ್ಗೆ': 'about', 'बारे': 'about', 'பற்றி': 'about', 'గురించి': 'about',
            'കുറിച്ച്': 'about', 'সম্পর্কে': 'about', 'વિશે': 'about', 'ਬਾਰੇ': 'about',
            
            # Tell / Show
            'बताओ': 'tell', 'சொல்லுங்கள்': 'tell', 'చెప్పండి': 'tell',
            'പറയൂ': 'tell', 'বলুন': 'tell', 'કહો': 'tell', 'ਦੱਸੋ': 'tell',
            'दिखाओ': 'show', 'காட்டு': 'show', 'చూపించు': 'show', 'കാണിക്കൂ': 'show',
            'দেখান': 'show', 'બતાવો': 'show', 'ਵਿਖਾਓ': 'show',
            
            # All
            'सभी': 'all', 'எல்லா': 'all', 'అన్ని': 'all', 'എല്ലാ': 'all',
            'সব': 'all', 'બધા': 'all', 'ਸਾਰੇ': 'all', 'ಎಲ್ಲಾ': 'all',
            
            # States
            'राज्य': 'states', 'மாநிலங்கள்': 'states', 'రాష్ట్రాలు': 'states',
            'സംസ്ഥാനങ്ങൾ': 'states', 'রাজ্য': 'states', 'રાજ્યો': 'states',
            'ਰਾਜ': 'states', 'ರಾಜ್ಯಗಳು': 'states',
            
            # Rainfall / Rain
            'वर्षा': 'rainfall', 'மழை': 'rainfall', 'వర్షపాతం': 'rainfall',
            'മഴ': 'rainfall', 'বৃষ্টিপাত': 'rainfall', 'વરસાદ': 'rainfall',
            'ਬਾਰਿਸ਼': 'rainfall', 'ಮಳೆ': 'rainfall', 'बारिश': 'rain',
            
            # Groundwater
            'भूजल': 'groundwater', 'நிலத்தடி நீர்': 'groundwater', 'భూగర్భ జలం': 'groundwater',
            'ഭൂഗർഭജലം': 'groundwater', 'ভূগর্ভস্থ জল': 'groundwater', 'ભૂગર્ભજળ': 'groundwater',
            'ਭੂਮੀਗਤ ਪਾਣੀ': 'groundwater', 'ಭೂಗರ್ಭ ನೀರು': 'groundwater',
            
            # Extraction
            'निष्कर्षण': 'extraction', 'பிரித்தெடுத்தல்': 'extraction', 'వెలికితీత': 'extraction',
            'ഉത്സർഗം': 'extraction', 'নিষ্কাশন': 'extraction', 'નિષ્કર્ષણ': 'extraction',
            
            # Compare
            'तुलना': 'compare', 'ஒப்பீடு': 'compare', 'పోల్చండి': 'compare',
            'താരതമ്യം': 'compare', 'তুলনা': 'compare', 'તુલના': 'compare',
            'ತುಲನೆ': 'compare',
            
            # District
            'जिला': 'district', 'மாவட்டம்': 'district', 'జిల్లా': 'district',
            'ജില്ല': 'district', 'জেলা': 'district', 'જિલ્લો': 'district',
            'ಜಿಲ್ಲೆ': 'district',
        }
    
    def translate_text(self, text: str, target_language: str, source_language: str = 'auto') -> str:
        """Translate text using deep-translator with comprehensive keyword mapping"""
        if not text or not text.strip():
            return text
        
        try:
            # Apply keyword mapping first (most accurate for location names)
            mapped_text = self._apply_keyword_mapping(text)
            if mapped_text != text:
                logger.info(f"Keyword mapped: '{text}' -> '{mapped_text}'")
                text = mapped_text
            
            # If already in target language, return
            if target_language == 'en' and source_language == 'en':
                return text
            
            # Try deep-translator
            translated = GoogleTranslator(source=source_language, target=target_language).translate(text)
            
            if translated and translated != text:
                logger.info(f"Translated: '{text}' -> '{translated}'")
                return translated
            
            return text
            
        except Exception as e:
            logger.error(f"Translation error: {e}")
            return self._apply_keyword_mapping(text)
    
    def _apply_keyword_mapping(self, text: str) -> str:
        """Map non-English keywords to English"""
        result = text
        # Sort by length (longest first) to match longer phrases first
        sorted_mappings = sorted(self.keyword_map.items(), key=lambda x: len(x[0]), reverse=True)
        for native, english in sorted_mappings:
            if native in result:
                result = result.replace(native, english)
        return result
    
    def detect_language(self, text: str) -> str:
        """Detect language based on Unicode character ranges"""
        try:
            if not text or not text.strip():
                return 'en'
            
            # Check for specific script ranges
            if any('\u0900' <= char <= '\u097F' for char in text):  # Devanagari (Hindi/Marathi)
                return 'hi'
            elif any('\u0C80' <= char <= '\u0CFF' for char in text):  # Kannada
                return 'kn'
            elif any('\u0B80' <= char <= '\u0BFF' for char in text):  # Tamil
                return 'ta'
            elif any('\u0C00' <= char <= '\u0C7F' for char in text):  # Telugu
                return 'te'
            elif any('\u0D00' <= char <= '\u0D7F' for char in text):  # Malayalam
                return 'ml'
            elif any('\u0A80' <= char <= '\u0AFF' for char in text):  # Gujarati
                return 'gu'
            elif any('\u0980' <= char <= '\u09FF' for char in text):  # Bengali
                return 'bn'
            elif any('\u0A00' <= char <= '\u0A7F' for char in text):  # Gurmukhi (Punjabi)
                return 'pa'
            
            return 'en'
            
        except Exception as e:
            logger.error(f"Language detection error: {e}")
            return 'en'

translator = TranslationService()
