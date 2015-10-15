import pymongo
import config
import uuid

conn = pymongo.MongoClient(config.config['mongo_url'])

def get_images():
    images = []
    db = conn.docker_manager
    coll = db.images
    unpro = coll.find()
    for doc in unpro:
        doc.pop('_id')
        images.append(doc['name'])
    return images

def get_my_images(username):
    images = []
    db = conn.docker_manager
    coll = db.my_images
    unpro = coll.find({'user': username})
    for doc in unpro:
        doc.pop('_id')
        doc['full_name'] = doc['user'] + "/" + doc['name'] + ":" + '.'.join(str(doc['version']))
        images.append(doc)
        
    return images

def save_images(image):
    db = conn.docker_manager
    coll = db.images
    image['image_id'] = str(uuid.uuid4())
    coll.save(image)
    
def save_my_images(image):
    db = conn.docker_manager
    coll = db.my_images
    image['image_id'] = str(uuid.uuid4())
    coll.save(image)
    
def delete_images(name):
    db = conn.docker_manager
    coll = db.images
    coll.delete_one({'image_id': name})
    coll.delete_one({'name': name})
    
def delete_my_images(user, name):
    db = conn.docker_manager
    coll = db.my_images
    coll.delete_one({'user': user, 'image_id': name})
    coll.delete_one({'user': user, 'name': name})

def get_projects():
    images = []
    db = conn.docker_manager
    coll = db.projects
    unpro = coll.find()
    for doc in unpro:
        item = {"project_id": doc['project_id'], 'name': doc['name']}
        images.append(item)
    return images

def get_project_info(project_id):
    db = conn.docker_manager
    coll = db.projects
    unpro = coll.find_one({'project_id': project_id})
    if unpro:
        unpro.pop('_id')
    return unpro

def save_project(project):
    db = conn.docker_manager
    coll = db.projects
    project['project_id'] = str(uuid.uuid4())
    coll.save(project)
    
def update_project(project):
    db = conn.docker_manager
    coll = db.projects
    pid = project["project_id"]
    if not pid:
        return
    arch = project['arch']
    if arch:
        coll.update_one({'project_id': pid}, {'$set': {'arch': arch}})
    
    name = project['name']
    if name:
        coll.update_one({'project_id': pid}, {'$set': {'name': name}})
        
        
def get_image_version(user, name):
    db = conn.docker_manager
    coll = db.my_images
    image = coll.find({'user': user, 'name': name}).sort('version', pymongo.DESCENDING)
    version = 100
    for c in image:
        version = c['version']
        break
    
    return version

def delete_project(project_id):
    db = conn.docker_manager
    coll = db.projects
    coll.delete_one({'project_id': project_id})
    
def get_clusters():
    images = []
    db = conn.docker_manager
    coll = db.clusters
    unpro = coll.find()
    for doc in unpro:
        doc.pop('_id')
        images.append(doc)
    return images

def add_cluster(cluster):
    db = conn.docker_manager
    coll = db.clusters
    cluster['cluster_id'] = str(uuid.uuid4())
    coll.save(cluster)
    
def delete_cluster(name):
    db = conn.docker_manager
    coll = db.clusters
    coll.delete_one({'cluster_id': name})
    coll.delete_one({'name': name})
    
    