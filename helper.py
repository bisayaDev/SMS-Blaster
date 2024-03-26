import json

def group_data_by(data, n):
    items_per_group, extras = divmod(len(data), n)

    # Prepare the output list
    result = []
    start = 0

    for i in range(n):
        # Calculate the number of items for the current group
        end = start + items_per_group + (1 if i < extras else 0)
        # Append the current slice of data to the result list
        result.append(data[start:end])
        # Update the start index for the next group
        start = end

    return result

def fix_cp_numbers(num):
    if num.startswith('09') and len(num) == 11:
        return num
    elif num.startswith('+639') and len(num) == 13:
        return num
    elif num.startswith('639') and len(num) == 12:
        return num
    elif num.startswith('9') and len(num) == 10:
        return f"0{num}"
    else:
        return False

def trim_data(data):
    json_data = json.loads(data)
    return json_data

def dummy_data(job_id):
    dd = [
            {
              "id": 1,
              "text": "Lorem ipsum dolor sit amet, consectetuer adipiscing elit.",
              "phone_number": "09845289262",
              "url": "https://staging.ecitizenph.com/",
              "job_id": 99,
              "base_url": "staging"
            }, {
              "id": 2,
              "text": "Fusce congue, diam id ornare imperdiet, sapien urna pretium nisl, ut volutpat sapien arcu sed augue.",
              "phone_number": "09835652964",
              "url": "https://staging.ecitizenph.com/",
              "job_id": 99,
              "base_url": "staging"
            }, {
              "id": 3,
              "text": "Morbi vel lectus in quam fringilla rhoncus.",
              "phone_number": "09191757343",
              "url": "https://staging.ecitizenph.com/",
              "job_id": 99,
              "base_url": "staging"
            }, {
              "id": 4,
              "text": "Integer ac leo.",
              "phone_number": "09962851911",
              "url": "https://staging.ecitizenph.com/",
              "job_id": 99,
              "base_url": "staging"
            }, {
              "id": 5,
              "text": "Etiam vel augue.",
              "phone_number": "09321258574",
              "url": "https://staging.ecitizenph.com/",
              "job_id": 99,
              "base_url": "staging"
            }, {
              "id": 6,
              "text": "Nullam porttitor lacus at turpis.",
              "phone_number": "1723030351",
              "url": "https://staging.ecitizenph.com/",
              "job_id": 99,
              "base_url": "staging"
            }, {
              "id": 7,
              "text": "Vivamus metus arcu, adipiscing molestie, hendrerit at, vulputate vitae, nisl.",
              "phone_number": "09124711841",
              "url": "https://staging.ecitizenph.com/",
              "job_id": 99,
              "base_url": "staging"
            }, {
              "id": 8,
              "text": "Cum sociis natoque penatibus et magnis dis parturient montes, nascetur ridiculus mus.",
              "phone_number": "9148812476",
              "url": "https://staging.ecitizenph.com/",
              "job_id": 99,
              "base_url": "staging"
            }, {
              "id": 9,
              "text": "Sed accumsan felis.",
              "phone_number": "09231709323",
              "url": "https://staging.ecitizenph.com/",
              "job_id": 99,
              "base_url": "staging"
            }, {
              "id": 10,
              "text": "In hac habitasse platea dictumst.",
              "phone_number": "09542979114",
              "url": "https://staging.ecitizenph.com/",
              "job_id": 99,
              "base_url": "staging"
            }
        ]
    for i in dd:
        i['job_id'] = job_id
        if i['id'] % 2 == 0:
            i['phone_number'] = "09655144910"
        else:
            i['phone_number'] = "09357632143"
    return dd
