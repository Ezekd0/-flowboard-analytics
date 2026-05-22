def format_date(date_obj):
    return date_obj.strftime("%Y-%m-%d %H:%M:%S") if date_obj else None

def format_task_response(task):
    return {
        "id": task.id,
        "title": task.title,
        "description": task.description,
        "status": task.status,
        "priority": task.priority,
        "created_at": format_date(task.created_at),
        "updated_at": format_date(task.updated_at)
    }
