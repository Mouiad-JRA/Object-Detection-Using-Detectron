# Object-Detection-Using-Detectron
# 2D object tracking learning and inferencing using Detectron2 

<img src="https://dl.fbaipublicfiles.com/detectron2/Detectron2-Logo-Horz.png" width="500">

Here, we will go through installing detectron2, including the following:
* Run inference on images with an existing detectron2 model
* Train a detectron2 model on a new dataset
*  evaluation 

You can make a copy of this project by "File -> Open in playground mode" and make changes there. __DO NOT__ request access to this project.
We first test an image from the our dataset:
Then, we create a detectron2 config and a detectron2 `DefaultPredictor` to run inference on this image.
<h1>Part one<h1>
# Train on our dataset (custom)
In this section, we show how to train an existing detectron2 model on a our dataset in a new format.
our dataset only has one class: Person.

#Register the our dataset to detectron2
## Train!
Now, let's fine-tune a COCO-pretrained all Zoo-model on our  dataset. It takes ~6 minutes to train 300 iterations on Colab's K80 GPU, or ~2 minutes on a P100 GPU.
Then
## Inference & evaluation using our trained model
Now, let's run inference with the trained model on the our validation dataset. First, we create a predictor using the model we just trained:

# We will evaluate the performance using AP metric implemented in COCO API.
# Then we are going to comper the result
<h1>Part two<h1>
link for the second data set is
http://aiskyeye.com/download/multi-object-tracking_2021/
