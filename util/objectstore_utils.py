import boto3
from dataclasses import dataclass
from operator import attrgetter
from io import BytesIO
#from boto3.resources.factory.s3 import ServiceResource


@dataclass
class S3AccessConf():
    """
    Examples:
        s3_conf = S3AccessConf(
            bucket_name = "xxx",
            access_key_id = os.environ.get('AWS_ACCESS_KEY_ID'),
            secret_access_key = os.environ.get('AWS_SECRET_ACCESS_KEY'),
            endpoint = os.environ.get('S3_ENDPOINT'),
            verify_host = True
        )    
    """
    access_key_id: str
    secret_access_key: str
    endpoint: str
    bucket_name: str
    verify_host: bool = True
    

class S3BucketHelper():
    # more about client caching
    def __init__(self, conf: S3AccessConf, file_prefix: str=""):
        """
        Args:
            file_prefix: s3 bucket objects key prefix used to filter the object
          
        Examples:
            S3BucketHelper(S3BucketConfig())
        """
        self.conf = conf      
        # session is the resource which can be passed around
        # https://github.com/boto/boto3/issues/3197#issuecomment-1180516179
        self.session = boto3.session.Session(
            aws_access_key_id = self.conf.access_key_id,
            aws_secret_access_key = self.conf.secret_access_key
        )
        self.file_prefix = file_prefix
 

    def _get_s3_resource(self):
        # resource is a s3 endpoint 
        s3 = self.session.resource('s3', endpoint_url = self.conf.endpoint, verify=self.conf.verify_host)
        return s3
    
            
    def get_object_keys(self, limit_count: int=-1) -> map:
        """
        Return:
            map generator object
        """
        # bucket_items = []
        s3 = self._get_s3_resource()
        bucket = s3.Bucket(self.conf.bucket_name)
        # for obj in bucket.objects.all():
        
        # Filter: https://boto3.amazonaws.com/v1/documentation/api/latest/guide/collections.html#filtering
        
        # https://stackoverflow.com/questions/45477181/apply-map-over-property-in-python
        # map object https://realpython.com/python-map-function/
        if limit_count < 0:
            bucket_items_map = map(attrgetter('key'), 
                    bucket.objects.filter(Prefix=self.file_prefix)
                   )
        else:
            bucket_items_map = map(attrgetter('key'), 
                    bucket.objects.filter(Prefix=self.file_prefix).limit(limit_count)
                   )
        return bucket_items_map
    
    # @staticmethod
    # def key_to_bytesio(s3: ServiceResource,  )
    
    def transform_objects(self, s3_keys: map, bytesio_transformer: callable) -> map:       
        # callable https://realpython.com/python-callable-instances/
        s3 = self._get_s3_resource()
        
        bytesio_map = map(lambda x: {
            "name" : x,
            "bytesio" : BytesIO(s3.Object(self.conf.bucket_name, x).get()['Body'].read())
        }, s3_keys)
        
        return map(bytesio_transformer, bytesio_map)   
