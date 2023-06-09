import pika, json

def upload(file, gfs, channel, access):
    try:
        res = gfs.put(file)
    except Exception as err:
        return "Failed to upload file.", 500
    
    message = {
        "img_fid": str(res),
        "username": access["username"],
    }

    try:
        channel.basic_publish(
            exchange="",
            routing_key="src_images",
            body=json.dumps(message),
            properties=pika.BasicProperties(
                delivery_mode=pika.spec.PERSISTENT_DELIVERY_MODE
            ),
        )
    except:
        gfs.delete(res)
        return "Internal server error", 500
