import pymongo

conn = pymongo.MongoClient('mongodb://vophoto-test.chinacloudapp.cn:27017/')

def get_images():
    images = []
    db = conn.docker_manager
    coll = db.images
    unpro = coll.find()
    for doc in unpro:
        images.append(doc['name'])
    return images

def get_projects():
    images = []
    db = conn.docker_manager
    coll = db.projects
    unpro = coll.find()
    for doc in unpro:
        images.append(doc['name'])
    return images

def get_project_info(project_id):
    db = conn.docker_manager
    coll = db.projects
    unpro = coll.find_one({'project_id': project_id})
    return unpro