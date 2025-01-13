

import graphene
from graphene_file_upload.scalars import Upload
from PIL import Image
import os

class UploadFileMutation(graphene.Mutation):
    class Arguments:
        file = Upload(required=True)

    success = graphene.Boolean()

    def mutate(self, info, file, **kwargs):
        file_name = file.name
        image = Image.open(file.file)
        save_path = os.path.join(os.getcwd(), 'images', file_name)    
        image.save(save_path)    
        return UploadFileMutation(success=True)

class Mutation(graphene.ObjectType):
    uploadFile = UploadFileMutation.Field()

class Query(graphene.ObjectType):
    hello = graphene.String()
    def resolve_hello(root, info):
        return "hello world"

schema = graphene.Schema(query=Query, mutation=Mutation)