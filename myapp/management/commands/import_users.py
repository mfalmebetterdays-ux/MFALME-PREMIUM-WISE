# myapp/management/commands/import_users.py
from django.core.management.base import BaseCommand
from django.contrib.auth.hashers import make_password
from myapp.models import Tradeviewusers
from datetime import datetime

class Command(BaseCommand):
    help = 'Import all 111 TradeWise users'

    def handle(self, *args, **options):
        self.stdout.write('🚀 Starting user import...')
        
        # Check if users already exist
        existing_count = Tradeviewusers.objects.count()
        if existing_count > 0:
            self.stdout.write(f'⚠️ Database already has {existing_count} users. Skipping import.')
            return
        
        # Your 111 users from the CSV
        users_data = [
            {'first_name': 'Meshack', 'second_name': 'Mwangi', 'email': 'meshmwangi88@gmail.com', 'account_number': 5000, 'phone': '0115721877', 'verified': False, 'admin': False, 'staff': False, 'created_at': '2025-11-29 18:36:48'},
            {'first_name': 'Meshack', 'second_name': 'Mwangi', 'email': 'meshmwangi828@gmail.com', 'account_number': 5001, 'phone': '0115721877', 'verified': False, 'admin': False, 'staff': False, 'created_at': '2025-11-29 18:43:32'},
            {'first_name': 'Mesh', 'second_name': 'Mwangi', 'email': 'brayanne800@gmail.com', 'account_number': 5002, 'phone': '0728538660', 'verified': False, 'admin': False, 'staff': False, 'created_at': '2025-11-29 18:56:20'},
            {'first_name': 'Spallis', 'second_name': 'Kinywero', 'email': 'manchamthreads@gmail.com', 'account_number': 5003, 'phone': '0748092931', 'verified': True, 'admin': False, 'staff': False, 'created_at': '2025-11-29 19:34:59'},
            {'first_name': 'Mesh-Dev', 'second_name': 'Kingz', 'email': 'manchamthreds@gmail.com', 'account_number': 5004, 'phone': '0115721877', 'verified': False, 'admin': False, 'staff': False, 'created_at': '2025-11-29 19:37:25'},
            {'first_name': 'Mesh-Dev', 'second_name': 'Kingz', 'email': 'manchamthads@gmail.com', 'account_number': 5005, 'phone': '0115721877', 'verified': False, 'admin': False, 'staff': False, 'created_at': '2025-11-29 20:47:02'},
            {'first_name': 'Mesh', 'second_name': 'Mpenda Haga', 'email': 'baharihomeske@gmail.com', 'account_number': 5006, 'phone': '0115721877', 'verified': False, 'admin': False, 'staff': False, 'created_at': '2025-11-30 01:43:04'},
            {'first_name': 'Mkuu', 'second_name': 'Mwangi', 'email': 'manchmdeveloers@gmail.com', 'account_number': 5007, 'phone': '0115721877', 'verified': False, 'admin': False, 'staff': False, 'created_at': '2025-11-30 05:21:17'},
            {'first_name': 'Training', 'second_name': 'Web', 'email': 'manchamskools@gmail.com', 'account_number': 5008, 'phone': '0115721877', 'verified': False, 'admin': False, 'staff': False, 'created_at': '2025-12-12 06:23:56'},
            {'first_name': 'Mesh', 'second_name': 'Mwangi', 'email': 'tradewise010@gmail.com', 'account_number': 5009, 'phone': '0728538660', 'verified': False, 'admin': False, 'staff': False, 'created_at': '2025-12-17 07:12:48'},
            {'first_name': 'System', 'second_name': 'Admin', 'email': 'system@tradewise.com', 'account_number': 500000, 'phone': None, 'verified': False, 'admin': True, 'staff': False, 'created_at': '2026-01-06 19:14:14'},
            {'first_name': 'Alex', 'second_name': 'Chebet', 'email': 'alex.chebet385@gmail.com', 'account_number': 500001, 'phone': '+25479889223', 'verified': True, 'admin': False, 'staff': False, 'created_at': '2026-03-02 19:51:58'},
            {'first_name': 'Faith', 'second_name': 'Atieno', 'email': 'faith.atieno592@gmail.com', 'account_number': 500002, 'phone': '+25478473956', 'verified': True, 'admin': False, 'staff': False, 'created_at': '2026-03-02 19:51:58'},
            {'first_name': 'Joseph', 'second_name': 'Atieno', 'email': 'joseph.atieno984@gmail.com', 'account_number': 500003, 'phone': '+25475535253', 'verified': True, 'admin': False, 'staff': False, 'created_at': '2026-03-02 19:51:59'},
            {'first_name': 'Elizabeth', 'second_name': 'Chebet', 'email': 'elizabeth.chebet560@gmail.com', 'account_number': 500004, 'phone': '+25479681310', 'verified': True, 'admin': False, 'staff': False, 'created_at': '2026-03-02 19:51:59'},
            {'first_name': 'Collins', 'second_name': 'Ouma', 'email': 'collins.ouma986@gmail.com', 'account_number': 500005, 'phone': '+25471273933', 'verified': True, 'admin': False, 'staff': False, 'created_at': '2026-03-02 19:51:59'},
            {'first_name': 'Brian', 'second_name': 'Wafula', 'email': 'brian.wafula782@gmail.com', 'account_number': 500006, 'phone': '+25471081871', 'verified': True, 'admin': False, 'staff': False, 'created_at': '2026-03-02 19:51:59'},
            {'first_name': 'Brenda', 'second_name': 'Odero', 'email': 'brenda.odero361@gmail.com', 'account_number': 500007, 'phone': '+25475261235', 'verified': True, 'admin': False, 'staff': False, 'created_at': '2026-03-02 19:51:59'},
            {'first_name': 'John', 'second_name': 'Omondi', 'email': 'john.omondi192@gmail.com', 'account_number': 500008, 'phone': '+25475273575', 'verified': True, 'admin': False, 'staff': False, 'created_at': '2026-03-02 19:52:00'},
            {'first_name': 'Sarah', 'second_name': 'Kipchoge', 'email': 'sarah.kipchoge57@gmail.com', 'account_number': 500009, 'phone': '+25473238590', 'verified': True, 'admin': False, 'staff': False, 'created_at': '2026-03-02 19:52:00'},
            {'first_name': 'Sarah', 'second_name': 'Wanjiku', 'email': 'sarah.wanjiku760@gmail.com', 'account_number': 500010, 'phone': '+25474292351', 'verified': True, 'admin': False, 'staff': False, 'created_at': '2026-03-02 19:52:00'},
            {'first_name': 'Brenda', 'second_name': 'Mutua', 'email': 'brenda.mutua301@gmail.com', 'account_number': 500011, 'phone': '+25479171791', 'verified': True, 'admin': False, 'staff': False, 'created_at': '2026-03-02 19:52:00'},
            {'first_name': 'Irene', 'second_name': 'Omondi', 'email': 'irene.omondi702@gmail.com', 'account_number': 500012, 'phone': '+25477345591', 'verified': True, 'admin': False, 'staff': False, 'created_at': '2026-03-02 19:52:00'},
            {'first_name': 'Irene', 'second_name': 'Chebet', 'email': 'irene.chebet12@gmail.com', 'account_number': 500013, 'phone': '+25472961034', 'verified': True, 'admin': False, 'staff': False, 'created_at': '2026-03-02 19:52:01'},
            {'first_name': 'Sarah', 'second_name': 'Muli', 'email': 'sarah.muli485@gmail.com', 'account_number': 500014, 'phone': '+25473886167', 'verified': True, 'admin': False, 'staff': False, 'created_at': '2026-03-02 19:52:01'},
            {'first_name': 'Lucy', 'second_name': 'Wekesa', 'email': 'lucy.wekesa923@gmail.com', 'account_number': 500015, 'phone': '+25479723369', 'verified': True, 'admin': False, 'staff': False, 'created_at': '2026-03-02 19:52:01'},
            {'first_name': 'Caroline', 'second_name': 'Okoth', 'email': 'caroline.okoth473@gmail.com', 'account_number': 500016, 'phone': '+25477712724', 'verified': True, 'admin': False, 'staff': False, 'created_at': '2026-03-02 19:52:01'},
            {'first_name': 'Caroline', 'second_name': 'Mutua', 'email': 'caroline.mutua138@gmail.com', 'account_number': 500017, 'phone': '+25478290244', 'verified': True, 'admin': False, 'staff': False, 'created_at': '2026-03-02 19:52:01'},
            {'first_name': 'Peter', 'second_name': 'Omondi', 'email': 'peter.omondi630@gmail.com', 'account_number': 500018, 'phone': '+25475257306', 'verified': True, 'admin': False, 'staff': False, 'created_at': '2026-03-02 19:52:01'},
            {'first_name': 'John', 'second_name': 'Njeri', 'email': 'john.njeri424@gmail.com', 'account_number': 500019, 'phone': '+25472249482', 'verified': True, 'admin': False, 'staff': False, 'created_at': '2026-03-02 19:52:02'},
            {'first_name': 'Eric', 'second_name': 'Omondi', 'email': 'eric.omondi1@gmail.com', 'account_number': 500020, 'phone': '+25479595085', 'verified': True, 'admin': False, 'staff': False, 'created_at': '2026-03-02 19:52:02'},
            {'first_name': 'Elizabeth', 'second_name': 'Wekesa', 'email': 'elizabeth.wekesa132@gmail.com', 'account_number': 500021, 'phone': '+25478023801', 'verified': True, 'admin': False, 'staff': False, 'created_at': '2026-03-02 19:52:03'},
            {'first_name': 'Ann', 'second_name': 'Mwangi', 'email': 'ann.mwangi348@gmail.com', 'account_number': 500022, 'phone': '+25471331369', 'verified': True, 'admin': False, 'staff': False, 'created_at': '2026-03-02 19:52:03'},
            {'first_name': 'Patrick', 'second_name': 'Chebet', 'email': 'patrick.chebet46@gmail.com', 'account_number': 500023, 'phone': '+25476542485', 'verified': True, 'admin': False, 'staff': False, 'created_at': '2026-03-02 19:52:03'},
            {'first_name': 'Esther', 'second_name': 'Kariuki', 'email': 'esther.kariuki266@gmail.com', 'account_number': 500024, 'phone': '+25478947395', 'verified': True, 'admin': False, 'staff': False, 'created_at': '2026-03-02 19:52:03'},
            {'first_name': 'Sharon', 'second_name': 'Njeri', 'email': 'sharon.njeri835@gmail.com', 'account_number': 500025, 'phone': '+25478874056', 'verified': True, 'admin': False, 'staff': False, 'created_at': '2026-03-02 19:52:03'},
            {'first_name': 'James', 'second_name': 'Opiyo', 'email': 'james.opiyo703@gmail.com', 'account_number': 500026, 'phone': '+25473202036', 'verified': True, 'admin': False, 'staff': False, 'created_at': '2026-03-02 19:52:03'},
            {'first_name': 'Eric', 'second_name': 'Odhiambo', 'email': 'eric.odhiambo358@gmail.com', 'account_number': 500027, 'phone': '+25472715922', 'verified': True, 'admin': False, 'staff': False, 'created_at': '2026-03-02 19:52:04'},
            {'first_name': 'Alex', 'second_name': 'Omondi', 'email': 'alex.omondi925@gmail.com', 'account_number': 500028, 'phone': '+25475878114', 'verified': True, 'admin': False, 'staff': False, 'created_at': '2026-03-02 19:52:04'},
            {'first_name': 'Alex', 'second_name': 'Njeri', 'email': 'alex.njeri82@gmail.com', 'account_number': 500029, 'phone': '+25479043740', 'verified': True, 'admin': False, 'staff': False, 'created_at': '2026-03-02 19:52:04'},
            {'first_name': 'Elizabeth', 'second_name': 'Wanjiku', 'email': 'elizabeth.wanjiku385@gmail.com', 'account_number': 500030, 'phone': '+25473737268', 'verified': True, 'admin': False, 'staff': False, 'created_at': '2026-03-02 19:52:04'},
            {'first_name': 'Rose', 'second_name': 'Ouma', 'email': 'rose.ouma862@gmail.com', 'account_number': 500031, 'phone': '+25476205106', 'verified': True, 'admin': False, 'staff': False, 'created_at': '2026-03-02 19:52:04'},
            {'first_name': 'John', 'second_name': 'Mutua', 'email': 'john.mutua643@gmail.com', 'account_number': 500032, 'phone': '+25472884184', 'verified': True, 'admin': False, 'staff': False, 'created_at': '2026-03-02 19:52:05'},
            {'first_name': 'Eric', 'second_name': 'Chebet', 'email': 'eric.chebet756@gmail.com', 'account_number': 500033, 'phone': '+25477600831', 'verified': True, 'admin': False, 'staff': False, 'created_at': '2026-03-02 19:52:05'},
            {'first_name': 'Sharon', 'second_name': 'Opiyo', 'email': 'sharon.opiyo798@gmail.com', 'account_number': 500034, 'phone': '+25478004081', 'verified': True, 'admin': False, 'staff': False, 'created_at': '2026-03-02 19:52:05'},
            {'first_name': 'James', 'second_name': 'Wafula', 'email': 'james.wafula756@gmail.com', 'account_number': 500035, 'phone': '+25472993151', 'verified': True, 'admin': False, 'staff': False, 'created_at': '2026-03-02 19:52:05'},
            {'first_name': 'Sarah', 'second_name': 'Mutua', 'email': 'sarah.mutua836@gmail.com', 'account_number': 500036, 'phone': '+25477346242', 'verified': True, 'admin': False, 'staff': False, 'created_at': '2026-03-02 19:52:05'},
            {'first_name': 'David', 'second_name': 'Wekesa', 'email': 'david.wekesa67@gmail.com', 'account_number': 500037, 'phone': '+25477963659', 'verified': True, 'admin': False, 'staff': False, 'created_at': '2026-03-02 19:52:06'},
            {'first_name': 'Lucy', 'second_name': 'Awuor', 'email': 'lucy.awuor132@gmail.com', 'account_number': 500038, 'phone': '+25475744529', 'verified': True, 'admin': False, 'staff': False, 'created_at': '2026-03-02 19:52:06'},
            {'first_name': 'Rose', 'second_name': 'Njeri', 'email': 'rose.njeri789@gmail.com', 'account_number': 500039, 'phone': '+25473955165', 'verified': True, 'admin': False, 'staff': False, 'created_at': '2026-03-02 19:52:06'},
            {'first_name': 'Patrick', 'second_name': 'Odero', 'email': 'patrick.odero181@gmail.com', 'account_number': 500040, 'phone': '+25475698417', 'verified': True, 'admin': False, 'staff': False, 'created_at': '2026-03-02 19:52:07'},
            {'first_name': 'James', 'second_name': 'Wanjala', 'email': 'james.wanjala478@gmail.com', 'account_number': 500041, 'phone': '+25474045999', 'verified': True, 'admin': False, 'staff': False, 'created_at': '2026-03-02 19:52:07'},
            {'first_name': 'Michael', 'second_name': 'Kipchoge', 'email': 'michael.kipchoge91@gmail.com', 'account_number': 500042, 'phone': '+25473185758', 'verified': True, 'admin': False, 'staff': False, 'created_at': '2026-03-02 19:52:07'},
            {'first_name': 'Diana', 'second_name': 'Muli', 'email': 'diana.muli929@gmail.com', 'account_number': 500043, 'phone': '+25474045283', 'verified': True, 'admin': False, 'staff': False, 'created_at': '2026-03-02 19:52:07'},
            {'first_name': 'Elizabeth', 'second_name': 'Wanjiku', 'email': 'elizabeth.wanjiku250@gmail.com', 'account_number': 500044, 'phone': '+25472474190', 'verified': True, 'admin': False, 'staff': False, 'created_at': '2026-03-02 19:52:07'},
            {'first_name': 'Caroline', 'second_name': 'Odero', 'email': 'caroline.odero145@gmail.com', 'account_number': 500045, 'phone': '+25475625916', 'verified': True, 'admin': False, 'staff': False, 'created_at': '2026-03-02 19:52:08'},
            {'first_name': 'Diana', 'second_name': 'Ouma', 'email': 'diana.ouma719@gmail.com', 'account_number': 500046, 'phone': '+25479448521', 'verified': True, 'admin': False, 'staff': False, 'created_at': '2026-03-02 19:52:08'},
            {'first_name': 'Ann', 'second_name': 'Owuor', 'email': 'ann.owuor857@gmail.com', 'account_number': 500047, 'phone': '+25473104040', 'verified': True, 'admin': False, 'staff': False, 'created_at': '2026-03-02 19:52:08'},
            {'first_name': 'Diana', 'second_name': 'Otieno', 'email': 'diana.otieno950@gmail.com', 'account_number': 500048, 'phone': '+25476136145', 'verified': True, 'admin': False, 'staff': False, 'created_at': '2026-03-02 19:52:08'},
            {'first_name': 'Faith', 'second_name': 'Wekesa', 'email': 'faith.wekesa558@gmail.com', 'account_number': 500049, 'phone': '+25474462550', 'verified': True, 'admin': False, 'staff': False, 'created_at': '2026-03-02 19:52:09'},
            {'first_name': 'Kevin', 'second_name': 'Otieno', 'email': 'kevin.otieno895@gmail.com', 'account_number': 500050, 'phone': '+25475097490', 'verified': True, 'admin': False, 'staff': False, 'created_at': '2026-03-02 19:52:09'},
            {'first_name': 'Michael', 'second_name': 'Otieno', 'email': 'michael.otieno454@gmail.com', 'account_number': 500051, 'phone': '+25477155301', 'verified': True, 'admin': False, 'staff': False, 'created_at': '2026-03-02 19:52:09'},
            {'first_name': 'John', 'second_name': 'Opiyo', 'email': 'john.opiyo873@gmail.com', 'account_number': 500052, 'phone': '+25477740050', 'verified': True, 'admin': False, 'staff': False, 'created_at': '2026-03-02 19:52:09'},
            {'first_name': 'Eric', 'second_name': 'Ouma', 'email': 'eric.ouma36@gmail.com', 'account_number': 500053, 'phone': '+25477263545', 'verified': True, 'admin': False, 'staff': False, 'created_at': '2026-03-02 19:52:09'},
            {'first_name': 'Lucy', 'second_name': 'Ouma', 'email': 'lucy.ouma360@gmail.com', 'account_number': 500054, 'phone': '+25474788934', 'verified': True, 'admin': False, 'staff': False, 'created_at': '2026-03-02 19:52:09'},
            {'first_name': 'Patrick', 'second_name': 'Achieng', 'email': 'patrick.achieng961@gmail.com', 'account_number': 500055, 'phone': '+25471313541', 'verified': True, 'admin': False, 'staff': False, 'created_at': '2026-03-02 19:52:10'},
            {'first_name': 'Brian', 'second_name': 'Chebet', 'email': 'brian.chebet709@gmail.com', 'account_number': 500056, 'phone': '+25477979023', 'verified': True, 'admin': False, 'staff': False, 'created_at': '2026-03-02 19:52:10'},
            {'first_name': 'Joseph', 'second_name': 'Opiyo', 'email': 'joseph.opiyo545@gmail.com', 'account_number': 500057, 'phone': '+25476093679', 'verified': True, 'admin': False, 'staff': False, 'created_at': '2026-03-02 19:52:10'},
            {'first_name': 'Patrick', 'second_name': 'Awuor', 'email': 'patrick.awuor915@gmail.com', 'account_number': 500058, 'phone': '+25473835362', 'verified': True, 'admin': False, 'staff': False, 'created_at': '2026-03-02 19:52:10'},
            {'first_name': 'Catherine', 'second_name': 'Kipchoge', 'email': 'catherine.kipchoge557@gmail.com', 'account_number': 500059, 'phone': '+25479002046', 'verified': True, 'admin': False, 'staff': False, 'created_at': '2026-03-02 19:52:10'},
            {'first_name': 'Kevin', 'second_name': 'Awuor', 'email': 'kevin.awuor531@gmail.com', 'account_number': 500060, 'phone': '+25476137719', 'verified': True, 'admin': False, 'staff': False, 'created_at': '2026-03-02 19:52:11'},
            {'first_name': 'Alex', 'second_name': 'Wamalwa', 'email': 'alex.wamalwa858@gmail.com', 'account_number': 500061, 'phone': '+25478109401', 'verified': True, 'admin': False, 'staff': False, 'created_at': '2026-03-02 19:52:11'},
            {'first_name': 'James', 'second_name': 'Ouma', 'email': 'james.ouma515@gmail.com', 'account_number': 500062, 'phone': '+25477537101', 'verified': True, 'admin': False, 'staff': False, 'created_at': '2026-03-02 19:52:12'},
            {'first_name': 'Samuel', 'second_name': 'Kipchoge', 'email': 'samuel.kipchoge982@gmail.com', 'account_number': 500063, 'phone': '+25473024123', 'verified': True, 'admin': False, 'staff': False, 'created_at': '2026-03-02 19:52:12'},
            {'first_name': 'Mary', 'second_name': 'Awuor', 'email': 'mary.awuor235@gmail.com', 'account_number': 500064, 'phone': '+25478386139', 'verified': True, 'admin': False, 'staff': False, 'created_at': '2026-03-02 19:52:12'},
            {'first_name': 'Brenda', 'second_name': 'Akinyi', 'email': 'brenda.akinyi218@gmail.com', 'account_number': 500065, 'phone': '+25475860274', 'verified': True, 'admin': False, 'staff': False, 'created_at': '2026-03-02 19:52:12'},
            {'first_name': 'Sarah', 'second_name': 'Mwangi', 'email': 'sarah.mwangi818@gmail.com', 'account_number': 500066, 'phone': '+25473900831', 'verified': True, 'admin': False, 'staff': False, 'created_at': '2026-03-02 19:52:13'},
            {'first_name': 'Faith', 'second_name': 'Wanjiku', 'email': 'faith.wanjiku771@gmail.com', 'account_number': 500067, 'phone': '+25475735922', 'verified': True, 'admin': False, 'staff': False, 'created_at': '2026-03-02 19:52:13'},
            {'first_name': 'Diana', 'second_name': 'Kariuki', 'email': 'diana.kariuki127@gmail.com', 'account_number': 500068, 'phone': '+25472396584', 'verified': True, 'admin': False, 'staff': False, 'created_at': '2026-03-02 19:52:13'},
            {'first_name': 'Eric', 'second_name': 'Kipchoge', 'email': 'eric.kipchoge26@gmail.com', 'account_number': 500069, 'phone': '+25472969920', 'verified': True, 'admin': False, 'staff': False, 'created_at': '2026-03-02 19:52:13'},
            {'first_name': 'Brenda', 'second_name': 'Owuor', 'email': 'brenda.owuor373@gmail.com', 'account_number': 500070, 'phone': '+25477304396', 'verified': True, 'admin': False, 'staff': False, 'created_at': '2026-03-02 19:52:13'},
            {'first_name': 'John', 'second_name': 'Wafula', 'email': 'john.wafula199@gmail.com', 'account_number': 500071, 'phone': '+25471061165', 'verified': True, 'admin': False, 'staff': False, 'created_at': '2026-03-02 19:52:14'},
            {'first_name': 'Patrick', 'second_name': 'Owuor', 'email': 'patrick.owuor188@gmail.com', 'account_number': 500072, 'phone': '+25478597583', 'verified': True, 'admin': False, 'staff': False, 'created_at': '2026-03-02 19:52:14'},
            {'first_name': 'Brenda', 'second_name': 'Wafula', 'email': 'brenda.wafula326@gmail.com', 'account_number': 500073, 'phone': '+25478293204', 'verified': True, 'admin': False, 'staff': False, 'created_at': '2026-03-02 19:52:14'},
            {'first_name': 'Grace', 'second_name': 'Odero', 'email': 'grace.odero420@gmail.com', 'account_number': 500074, 'phone': '+25479823889', 'verified': True, 'admin': False, 'staff': False, 'created_at': '2026-03-02 19:52:14'},
            {'first_name': 'Eric', 'second_name': 'Mutua', 'email': 'eric.mutua200@gmail.com', 'account_number': 500075, 'phone': '+25477483188', 'verified': True, 'admin': False, 'staff': False, 'created_at': '2026-03-02 19:52:15'},
            {'first_name': 'Vincent', 'second_name': 'Okoth', 'email': 'vincent.okoth109@gmail.com', 'account_number': 500076, 'phone': '+25473422021', 'verified': True, 'admin': False, 'staff': False, 'created_at': '2026-03-02 19:52:15'},
            {'first_name': 'Eric', 'second_name': 'Owuor', 'email': 'eric.owuor68@gmail.com', 'account_number': 500077, 'phone': '+25471371965', 'verified': True, 'admin': False, 'staff': False, 'created_at': '2026-03-02 19:52:15'},
            {'first_name': 'Lucy', 'second_name': 'Omondi', 'email': 'lucy.omondi745@gmail.com', 'account_number': 500078, 'phone': '+25474949409', 'verified': True, 'admin': False, 'staff': False, 'created_at': '2026-03-02 19:52:15'},
            {'first_name': 'Ann', 'second_name': 'Mwangi', 'email': 'ann.mwangi905@gmail.com', 'account_number': 500079, 'phone': '+25479153210', 'verified': True, 'admin': False, 'staff': False, 'created_at': '2026-03-02 19:52:15'},
            {'first_name': 'Rose', 'second_name': 'Chebet', 'email': 'rose.chebet127@gmail.com', 'account_number': 500080, 'phone': '+25478619894', 'verified': True, 'admin': False, 'staff': False, 'created_at': '2026-03-02 19:52:16'},
            {'first_name': 'Vincent', 'second_name': 'Ouma', 'email': 'vincent.ouma434@gmail.com', 'account_number': 500081, 'phone': '+25474426110', 'verified': True, 'admin': False, 'staff': False, 'created_at': '2026-03-02 19:52:16'},
            {'first_name': 'Elizabeth', 'second_name': 'Mwangi', 'email': 'elizabeth.mwangi761@gmail.com', 'account_number': 500082, 'phone': '+25472525516', 'verified': True, 'admin': False, 'staff': False, 'created_at': '2026-03-02 19:52:16'},
            {'first_name': 'Brian', 'second_name': 'Chebet', 'email': 'brian.chebet960@gmail.com', 'account_number': 500083, 'phone': '+25472925626', 'verified': True, 'admin': False, 'staff': False, 'created_at': '2026-03-02 19:52:16'},
            {'first_name': 'Joseph', 'second_name': 'Odero', 'email': 'joseph.odero250@gmail.com', 'account_number': 500084, 'phone': '+25478247076', 'verified': True, 'admin': False, 'staff': False, 'created_at': '2026-03-02 19:52:16'},
            {'first_name': 'Daniel', 'second_name': 'Atieno', 'email': 'daniel.atieno385@gmail.com', 'account_number': 500085, 'phone': '+25473031307', 'verified': True, 'admin': False, 'staff': False, 'created_at': '2026-03-02 19:52:16'},
            {'first_name': 'Vincent', 'second_name': 'Onyango', 'email': 'vincent.onyango985@gmail.com', 'account_number': 500086, 'phone': '+25479422836', 'verified': True, 'admin': False, 'staff': False, 'created_at': '2026-03-02 19:52:17'},
            {'first_name': 'David', 'second_name': 'Njeri', 'email': 'david.njeri475@gmail.com', 'account_number': 500087, 'phone': '+25473204231', 'verified': True, 'admin': False, 'staff': False, 'created_at': '2026-03-02 19:52:18'},
            {'first_name': 'Caroline', 'second_name': 'Kariuki', 'email': 'caroline.kariuki540@gmail.com', 'account_number': 500088, 'phone': '+25476663365', 'verified': True, 'admin': False, 'staff': False, 'created_at': '2026-03-02 19:52:18'},
            {'first_name': 'David', 'second_name': 'Awuor', 'email': 'david.awuor940@gmail.com', 'account_number': 500089, 'phone': '+25471449173', 'verified': True, 'admin': False, 'staff': False, 'created_at': '2026-03-02 19:52:18'},
            {'first_name': 'Sarah', 'second_name': 'Mutua', 'email': 'sarah.mutua301@gmail.com', 'account_number': 500090, 'phone': '+25471348544', 'verified': True, 'admin': False, 'staff': False, 'created_at': '2026-03-02 19:52:18'},
            {'first_name': 'Peter', 'second_name': 'Muli', 'email': 'peter.muli504@gmail.com', 'account_number': 500091, 'phone': '+25474332804', 'verified': True, 'admin': False, 'staff': False, 'created_at': '2026-03-02 19:52:18'},
            {'first_name': 'Eric', 'second_name': 'Onyango', 'email': 'eric.onyango944@gmail.com', 'account_number': 500092, 'phone': '+25475269232', 'verified': True, 'admin': False, 'staff': False, 'created_at': '2026-03-02 19:52:18'},
            {'first_name': 'Patrick', 'second_name': 'Wamalwa', 'email': 'patrick.wamalwa288@gmail.com', 'account_number': 500093, 'phone': '+25477298712', 'verified': True, 'admin': False, 'staff': False, 'created_at': '2026-03-02 19:52:19'},
            {'first_name': 'Sharon', 'second_name': 'Onyango', 'email': 'sharon.onyango286@gmail.com', 'account_number': 500094, 'phone': '+25471643956', 'verified': True, 'admin': False, 'staff': False, 'created_at': '2026-03-02 19:52:19'},
            {'first_name': 'Vincent', 'second_name': 'Achieng', 'email': 'vincent.achieng123@gmail.com', 'account_number': 500095, 'phone': '+25476325765', 'verified': True, 'admin': False, 'staff': False, 'created_at': '2026-03-02 19:52:19'},
            {'first_name': 'Ann', 'second_name': 'Omondi', 'email': 'ann.omondi571@gmail.com', 'account_number': 500096, 'phone': '+25472904643', 'verified': True, 'admin': False, 'staff': False, 'created_at': '2026-03-02 19:52:20'},
            {'first_name': 'Ann', 'second_name': 'Wanjala', 'email': 'ann.wanjala136@gmail.com', 'account_number': 500097, 'phone': '+25478579072', 'verified': True, 'admin': False, 'staff': False, 'created_at': '2026-03-02 19:52:20'},
            {'first_name': 'Diana', 'second_name': 'Mutua', 'email': 'diana.mutua150@gmail.com', 'account_number': 500098, 'phone': '+25476023236', 'verified': True, 'admin': False, 'staff': False, 'created_at': '2026-03-02 19:52:20'},
            {'first_name': 'Lucy', 'second_name': 'Odero', 'email': 'lucy.odero84@gmail.com', 'account_number': 500099, 'phone': '+25473477475', 'verified': True, 'admin': False, 'staff': False, 'created_at': '2026-03-02 19:52:20'},
            {'first_name': 'Sarah', 'second_name': 'Atieno', 'email': 'sarah.atieno613@gmail.com', 'account_number': 500100, 'phone': '+25473632073', 'verified': True, 'admin': True, 'staff': True, 'created_at': '2026-03-02 19:52:21'}
        ]
        
        imported = 0
        for data in users_data:
            try:
                # Parse the created_at date
                created_at = datetime.strptime(data['created_at'], '%Y-%m-%d %H:%M:%S')
                
                # Create user
                user = Tradeviewusers(
                    first_name=data['first_name'],
                    second_name=data['second_name'],
                    email=data['email'],
                    account_number=data['account_number'],
                    phone=data['phone'],
                    is_active=True,
                    is_email_verified=data['verified'],
                    is_admin=data['admin'],
                    is_staff=data['staff'],
                    created_at=created_at,
                )
                # Set temporary password - users will reset this
                user.password = make_password('ResetMe@2025')
                user.save()
                
                imported += 1
                self.stdout.write(f'  ✅ {data["email"]}')
                
            except Exception as e:
                self.stdout.write(f'  ❌ {data["email"]}: {str(e)}')
        
        self.stdout.write(self.style.SUCCESS(f'\n🎉 Successfully imported {imported} users!'))
        self.stdout.write(self.style.WARNING('🔑 Temporary password for ALL users: ResetMe@2025'))
        self.stdout.write(self.style.WARNING('📝 Users MUST reset password on first login'))