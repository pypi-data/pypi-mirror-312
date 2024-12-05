from . import *

class Streets(BASE,Template):
	__tablename__="Streets"
	StreetId=Column(Integer,primary_key=True)
	StreetAddressRole=Column(String,default="What is this addressed used as/Business/Company/Organization Name, etc...(If Any)")
	StreetAddress=Column(String,default='Street Address(If Any)')
	StreetAddressOwner=Column(String,default='Street Address Owner(If Any)')
	StreetName=Column(String,default='Street Name(If Any)')
	City=Column(String,default='City Name(If Any)')
	State=Column(String,default='State of City(If Any)')
	ZipCode=Column(String,default='xxxxx-xxxx(If Any)')
	DTOE=Column(DateTime,default=datetime.now())

	def __init__(self,**kwargs):
		for k in kwargs.keys():
			if k in [s.name for s in self.__table__.columns]:
				setattr(self,k,kwargs.get(k))

class GeoTrip(BASE,Template):
	__tablename__="GeoTrip"
	gtid=Column(Integer,primary_key=True)

	StreetId=Column(Integer)
	TripName=Column(String)
	
	Latest=Column(Boolean,default=False)
	#none = not started
	#false = started and in progress
	#true = started and finished
	SearchState=Column(Boolean,default=None)

	#to calculate time taken
	SearchStartDT=Column(DateTime,default=None)
	SearchEndDT=Column(DateTime,default=None)

	#precise location data
	StartLatitude=Column(Integer)
	StartLongitude=Column(Integer)
	StartAltitude=Column(Integer)

	EndLatitude=Column(Integer)
	EndLongitude=Column(Integer)
	EndAltidude=Column(Integer)

	#actual distance traveled
	DistanceTraveled=Column(Float,default=0)
	#accumulated costs from trip
	TransitCostsTotal=Column(Float,default=0)

	DTOE=Column(DateTime,default=datetime.now())

	#what was used to make the trip for a vehicle, if any
	ModeOfTransit=Column(String,default="Bike")

	def __init__(self,**kwargs):
		for k in kwargs.keys():
			if k in [s.name for s in self.__table__.columns]:
				setattr(self,k,kwargs.get(k))

GeoTrip.metadata.create_all(ENGINE)
Streets.metadata.create_all(ENGINE)

class GeoMapClass:
	def import_odf(self):
		try:
			name=Path('Streets.ods')
			if name.exists():
				df=pd.read_excel(name)
				df.to_sql(Streets.__tablename__, ENGINE,if_exists='append',index=False)
			else:
				print(name,"does not exist!")
		except Exception as e:
			print(e,repr(e),str(e))


	def duplicateDelete(self):
		with Session(ENGINE) as session:
			sums=[]
			results=session.query(Streets).all()
			ct=len(results)
			
			for num,i in enumerate(results):
				SUM=hashlib.sha512()
				for col in i.__table__.columns:
					if str(col.type).lower() == "varchar":
						v=getattr(i,str(col.name))
						if not v:
							v=str(v)
						v=v.encode()
						SUM.update(v)
				if SUM.hexdigest() not in sums:
					sums.append(SUM.hexdigest())
				else:
					print(i)
					session.delete(i)
					session.commit()

	def randomStreet(self):
		with Session(ENGINE) as session:
			ALL=session.query(Streets).all()
			allCt=len(ALL)-1
			randomStreet=ALL[random.randint(0,allCt)]
			print(randomStreet)

	def add_street(self):
		excludes=[
		'StreetId',
		'DTOE'
		]
		with Session(ENGINE) as session:
			street=Streets()
			session.add(street)
			session.commit()
			session.refresh(street)
			dataCore={
				i.name:{
					'default':getattr(street,i.name),
					'type':str(i.type)
				} for i in Streets.__table__.columns if i.name not in excludes
			}
			fdata=FormBuilder(data=dataCore)
			if not fdata:
				session.delete(street)
				session.commit()
				msg="User abandoned!"
				print(msg)
				return
			
			for i in fdata:
				setattr(street,i,fdata[i])
			
			session.commit()
			session.refresh(street)
			print(street)
			self.duplicateDelete()

	def rm_street(self):
		ids=self.streetSearch(select=True)
		if ids in [None,]:
			return
		with Session(ENGINE) as session:
			for num,i in enumerate(ids):
				session.query(Streets).filter(Streets.StreetId==i).delete()
				if num % 100 == 0:
					session.commit()
			session.commit()

	def edit_street(self):
		ids=self.streetSearch(select=True)
		if ids in [None,]:
			return
		for ID in ids:
			excludes=[
			'StreetId',
			'DTOE'
			]
			with Session(ENGINE) as session:
				street=session.query(Streets).filter(Streets.StreetId==ID).first()
				if street:
					dataCore={
						i.name:{
							'default':getattr(street,i.name),
							'type':str(i.type)
						} for i in Streets.__table__.columns if i.name not in excludes
					}
					fdata=FormBuilder(data=dataCore)
					if not fdata:
						session.delete(street)
						session.commit()
						msg="User abandoned!"
						print(msg)
						return
					
					for i in fdata:
						setattr(street,i,fdata[i])
					
					session.commit()
					session.refresh(street)
					print(street)
					self.duplicateDelete()
				else:
					print(f"{Fore.light_red}Street was {Fore.orange_red_1}{street}{Style.reset}")

	def streetSearch(self,select=False):
		with Session(ENGINE) as session:
			search=Prompt.__init2__(None,func=FormBuilderMkText,ptext="What are you looking for? ",helpText="text that you are looking for",data="string")
			if search in [None,'d']:
				return
			fields=[i for i in Streets.__table__.columns if str(i.type) == "VARCHAR"]
			fields_2=[i.icontains(search) for i in fields]
			query=session.query(Streets)
			query=query.filter(or_(*fields_2))
			results=query.all()
			ct=len(results)
			if ct==0:
				print("no results!")
				return
			helpText=''
			for num,i in enumerate(results):
				msg=f'''{self.colorized(i,num,ct)}- {i}'''
				helpText+=f'{msg}\n'
				print(msg)
			if select:
				which=Prompt.__init2__(None,func=FormBuilderMkText,ptext="Which index(es[Comma Separated])",helpText=helpText,data="list")
				if which in [None,]:
					return
				elif which in [[],'d']:
					return []
				else:
					try:
						tmp=[]
						for i in which:
							try:
								INDEX=int(i)
								if INDEX in range(0,len(results)) and INDEX not in tmp:
									tmp.append(results[INDEX].StreetId)
							except Exception as ee:
								print(ee)
						return tmp
					except Exception as e:
						print(e)
					return []

	def colorized(self,i,num,ct):
		return f'{Fore.light_red}{num}{Fore.orange_red_1}/{Fore.light_green}{num+1} of {Fore.cyan}{ct} {Fore.magenta}'

	def listAllStreets(self):
		with Session(ENGINE) as session:
			results=session.query(Streets).all()
			ct=len(results)
			for num,i in enumerate(results):
				msg=f'''{self.colorized(i,num,ct)}- {i}'''
				print(msg)

	def exportStreetsODF(self):
		with Session(ENGINE) as session:
			query=session.query(Streets)
			df = pd.read_sql(query.statement, query.session.bind,dtype=str)
			df.to_excel("StreetsExport.ods",index=False)
			print(f"Saved to {Fore.light_green}StreetsExport.ods{Style.reset}")

	def clrStreets(self):
		with Session(ENGINE) as session:
			q=session.query(Streets).delete()
			session.commit()
		print("Streets Cleared!")

	def __init__(self):
		helpText=f'''
{Fore.medium_violet_red}"OSMTools"{Fore.orange_3} - Explore the World{Style.reset}
{Fore.light_cyan}'random street','rndmstrt','rstrt','xplr','get lost','get?'{Fore.light_red} -{Fore.dark_goldenrod} get a random street name to look for in the real world{Style.reset}
	
{Fore.light_cyan}'add streets','adstrts'{Fore.light_red} -{Fore.dark_goldenrod} [Manual] add a new street to db if it does not already exist{Style.reset}
{Fore.light_cyan}'rm streets','rmstrts'{Fore.light_red} -{Fore.dark_goldenrod} [Manual] delete a street from db {Style.reset}
{Fore.light_cyan}'edit streets','edstrts'{Fore.light_red} -{Fore.dark_goldenrod} [Manual] edit a street in db {Style.reset}
{Fore.light_cyan}'ls streets','lsstrts','las'{Fore.light_red} -{Fore.dark_goldenrod} List All Streets{Style.reset}
{Fore.light_cyan}'export streets odf','xpt strts odf','xsodf' -{Fore.dark_goldenrod} Export All Streets to ODF{Style.reset}
{Fore.light_cyan}'import streets odf','isodf'{Fore.light_red} -{Fore.dark_goldenrod} use an odf file to import streets using using ColumnsNames and Column Values{Style.reset}
{Fore.light_cyan}'clrdups','clear duplicates'{Fore.light_red} -{Fore.dark_goldenrod} search for duplicate Text entries in Streets{Style.reset}
{Fore.light_cyan}'clrstrts','clear streets','clear all streets','cas','cs'{Fore.light_red} -{Fore.dark_goldenrod} delete all streets from db{Style.reset}
{Fore.light_cyan}'ss','street search','strtsrch','search street'{Fore.light_red} -{Fore.dark_goldenrod} lookup a street from db{Style.reset}
{Fore.light_cyan}GeoTrip{Fore.light_magenta}[Not Implemented]{Style.reset}
		'''
		
		while True:
			action=Prompt.__init2__(None,func=FormBuilderMkText,ptext="OSMTools|Do What? ",helpText=helpText,data="string")
			if action in [None,]:
				return
			elif action in ['d',]:
				print(helpText)
			elif action.lower() in ['random street','rndmstrt','rstrt','xplr','get lost','get?']:
				self.randomStreet()
			elif action.lower() in ['add streets','adstrts']:
				self.add_street()
			elif action.lower() in ['rm streets','rmstrts']:
				self.rm_street()
			elif action.lower() in ['edit streets','edstrts']:
				self.edit_street()
			elif action.lower() in ['import streets odf','isodf']:
				self.import_odf()
				self.duplicateDelete()
			elif action.lower() in ['clrdups','clear duplicates']:
				self.duplicateDelete()
			elif action.lower() in ['clrstrts','clear streets','clear all streets','cas','cs']:
				self.clrStreets()
			elif action.lower() in ['ss','street search','strtsrch','search street']:
				self.streetSearch()
			elif action.lower() in ['ls streets','lsstrts','las']:
				self.listAllStreets()
			elif action.lower() in ['export streets odf','xpt strts odf','xsodf']:
				self.exportStreetsODF()