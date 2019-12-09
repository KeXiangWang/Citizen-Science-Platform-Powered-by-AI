import os
import json
import numpy as np
from keras.preprocessing.image import load_img
from keras.preprocessing.image import img_to_array
from keras.applications import inception_v3
from keras.applications import imagenet_utils

from django.http import JsonResponse


base_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)))


def judge(path):

    if not hasattr(judge, 'inception_model'):

        judge.inception_model = inception_v3.InceptionV3(weights='imagenet')

    if not hasattr(judge, 'label'):

        with open(os.path.join(base_dir, 'utils/ImageNet_Label.json'), 'r', encoding='utf-8') as file:

            judge.label = json.load(file)


    original = load_img(path, target_size=(299, 299))

    numpy_image = img_to_array(original)

    image_batch = np.expand_dims(numpy_image, axis=0)

    processed_image = inception_v3.preprocess_input(image_batch.copy())

    preds = judge.inception_model.predict(processed_image)

    print(imagenet_utils.decode_predictions(preds)[0])

    result = [judge.label.get(item[0], '其他') for item in imagenet_utils.decode_predictions(preds)[0]]

    return result


def judge_animal(request):

    msg = {'result': False}
    img = request.FILES.get('image')

    if not img:
        return JsonResponse(msg)

    postfix = img.name[img.name.rfind('.'):]
    if postfix not in ['.jpg', '.png', '.jpeg']:
        return JsonResponse(msg)

    with open(os.path.join(base_dir, 'static/tmp', img.name), 'wb') as file:
        for chunk in img.chunks():
            file.write(chunk)

    result = judge(os.path.join(base_dir, 'static/tmp', img.name))

    print(result)

    msg['result'] = '动物' in result

    os.remove(os.path.join(base_dir, 'static/tmp', img.name))

    return JsonResponse(msg)


def judge_fruit(request):

    msg = {'result': False}
    img = request.FILES.get('image')

    if not img:
        return JsonResponse(msg)

    postfix = img.name[img.name.rfind('.'):]
    if postfix not in ['.jpg', '.png', '.jpeg']:
        return JsonResponse(msg)

    with open(os.path.join(base_dir, 'static/tmp', img.name), 'wb') as file:
        for chunk in img.chunks():
            file.write(chunk)

    result = judge(os.path.join(base_dir, 'static/tmp', img.name))

    print(result)

    msg['result'] = '水果' in result

    os.remove(os.path.join(base_dir, 'static/tmp', img.name))

    return JsonResponse(msg)


def judge_tree(request):

    msg = {'result': False}
    img = request.FILES.get('image')

    if not img:
        return JsonResponse(msg)

    postfix = img.name[img.name.rfind('.'):]
    if postfix not in ['.jpg', '.png', '.jpeg']:
        return JsonResponse(msg)

    with open(os.path.join(base_dir, 'static/tmp', img.name), 'wb') as file:
        for chunk in img.chunks():
            file.write(chunk)

    result = judge(os.path.join(base_dir, 'static/tmp', img.name))

    print(result)

    msg['result'] = '植物' in result

    os.remove(os.path.join(base_dir, 'static/tmp', img.name))

    return JsonResponse(msg)
