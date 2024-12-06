import boto3,random,time,logging
from botocore.exceptions import ClientError
from datetime import datetime as d
from datetime import timedelta

class awsdjangoprod:

    aws_rds=boto3.client('rds',region_name="us-east-1")
    aws_sm=boto3.client('secretsmanager',region_name="us-east-1")

    DB_CREDENTIALS={}



    def create_rds_sm(self,Identifier=str,DBname=str,storage=int,DBinstancetype=str,Engine=str,Version=str,Public=bool,Securitygroup=list):

        self.DB_CREDENTIALS['DATABASES']=[{"IDENTIFIER":Identifier}]

        DBusername=input("enter an username for the rds:")
        DBpassword=input("enter a password for the rds:")

        response=self.aws_rds.create_db_instance(
        DBName=DBname,
        DBInstanceIdentifier=Identifier,
        AllocatedStorage=storage,
        DBInstanceClass=DBinstancetype,
        Engine=Engine,
        EngineVersion=Version,

        MasterUsername=DBusername,
        MasterUserPassword=DBpassword,

        Port=3306,
        MultiAZ=False,

        PubliclyAccessible=True,
        VpcSecurityGroupIds=Securitygroup
        )

        waiter = self.aws_rds.get_waiter('db_instance_available')

        waiter.wait(
        DBInstanceIdentifier=Identifier
        )

        try:
            temp=self.aws_sm.create_secret(
            Name='DBNAME',
            SecretString=DBname 
            )
            self.DB_CREDENTIALS['DATABASES'][0]['YOUR_DBNAME_FOR_SM']=temp['Name']
            time.sleep(5)
            


        except ClientError:
            res=''.join(str(d.now().timestamp()).split('.'))
            print('Name alreday exsits, modifying name....')
            print('New name is...')
            temp=self.aws_sm.create_secret(
            Name='DBNAME-'+res,
            SecretString=DBname
            )
            print(temp['Name'])
            self.DB_CREDENTIALS['DATABASES'][0]['YOUR_DBNAME_FOR_SM']=temp['Name']
            time.sleep(5)



        try:
            temp=self.aws_sm.create_secret(
            Name='DBUSERNAME',
            SecretString=DBusername
            )
            self.DB_CREDENTIALS['DATABASES'][0]['YOUR_DBUSERNAME_FOR_SM']=temp['Name']
            time.sleep(5)
            


        except ClientError:
            res=''.join(str(d.now().timestamp()).split('.'))
            print('Name alreday exsits, modifying name....')
            print('New name is...')
            temp=self.aws_sm.create_secret(
            Name='DBUSERNAME-'+res,
            SecretString=DBusername
            )
            print(temp['Name'])
            self.DB_CREDENTIALS['DATABASES'][0]['YOUR_DBUSERNAME_FOR_SM']=temp['Name']
            time.sleep(5)
            



        try:
            temp=self.aws_sm.create_secret(
            Name='DBPASSWORD',
            SecretString=DBpassword
            )
            self.DB_CREDENTIALS['DATABASES'][0]['YOUR_DBPASSWORD_FOR_SM']=temp['Name']
            time.sleep(5)
            



        except ClientError:
            res=''.join(str(d.now().timestamp()).split('.'))
            print('Name alreday exsits, modifying name....')
            print('New name is...')
            temp=self.aws_sm.create_secret(
            Name='DBPASSWORD-'+res,
            SecretString=DBpassword
            )
            print(temp['Name'])
            self.DB_CREDENTIALS['DATABASES'][0]['YOUR_DBPASSWORD_FOR_SM']=temp['Name']
            time.sleep(5)
            

        describe = self.aws_rds.describe_db_instances(
            DBInstanceIdentifier= Identifier
        )

        endpoint = describe["DBInstances"][-1]['Endpoint']['Address']

        try:
            temp=self.aws_sm.create_secret(
            Name='DBHOST',
            SecretString=endpoint
            )
            self.DB_CREDENTIALS['DATABASES'][0]['YOUR_DBHOST_FOR_SM']=temp['Name']


        except ClientError:
            res=''.join(str(d.now().timestamp()).split('.'))
            print('Name alreday exsits, modifying name....')
            print('New name is...')
            temp=self.aws_sm.create_secret(
            Name='DBHOST-'+res,
            SecretString=endpoint
            )
            self.DB_CREDENTIALS['DATABASES'][0]['YOUR_DBHOST_FOR_SM']=temp['Name']

        print(self.DB_CREDENTIALS)
        return response
        
    def djangosecretkey(self):
        key='!@#$^&*()_ABCDEFGHIJKLMNOPQRSTUVWXYZ-=+/<.>?0123456789;,:abcdefghijklmnopqrstuvwxyz[]'
        res=''

        for i in range(0,54):
            res+=key[random.randrange(0,84)]

        try:
            self.aws_sm.create_secret(
            Name='DJANGOSECRETKEY',
            SecretString=res
            )

        except ClientError:
            res=''.join(str(d.now().timestamp()).split('.'))
            print('Name alreday exsits, modifying name....')
            print('New name is...')
            self.aws_sm.create_secret(
            Name='DJANGOSECRETKEY-'+res,
            SecretString=res
            )

        return res

    def get_secret(self,name):
        secret_name = name
    
        client = boto3.client('secretsmanager',region_name="us-east-1")

        try:
            get_secret_value_response = client.get_secret_value(
            SecretId=secret_name
        )
        
        except ClientError as e:
            logging.error(e)

        return get_secret_value_response['SecretString']


    def delete_rds_sm(self,Identifier):
        response=self.aws_rds.describe_db_instances(
            DBInstanceIdentifier=Identifier
        )

        time1=response['DBInstances'][0]['InstanceCreateTime']

        zero_minutes=timedelta(minutes=0)
        ten_minutes = timedelta(minutes=10)

        secrets_list = self.aws_sm.list_secrets()        

        for i in secrets_list['SecretList']:
            res=self.aws_sm.describe_secret(
                SecretId=i['Name'])
            
            time2=res['CreatedDate']

            if zero_minutes<(time2-time1)<ten_minutes:
                if res['Name'].startswith('DB')==True:
                    print(self.aws_sm.delete_secret(
                    SecretId=res['Name'],
                    ))
        
        delete_response=self.aws_rds.delete_db_instance(
            DBInstanceIdentifier=Identifier,
            SkipFinalSnapshot=True)
        
        waiter = self.aws_rds.get_waiter('db_instance_deleted')

        waiter.wait(
        DBInstanceIdentifier=Identifier
        )

        return delete_response