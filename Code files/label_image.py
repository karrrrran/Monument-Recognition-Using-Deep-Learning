import tensorflow as tf
import sys

image_path = raw_input("Enter the path of the image: ")
#image_path = sys.argv[1]

# Store the image data which is provided in the path
image_data = tf.gfile.FastGFile(image_path, 'rb').read()

# Stores the labels of the classes of the images, and strips of the blank spaces
label_lines = [line.rstrip() for line 
                   in tf.gfile.GFile("/GoldenQuad/retrained_labels.txt")]

# Unpersists graph from file
with tf.gfile.FastGFile("/GoldenQuad/retrained_graph.pb", 'rb') as f:
    graph_def = tf.GraphDef()
    graph_def.ParseFromString(f.read())
    _ = tf.import_graph_def(graph_def, name='')

with tf.Session() as sess:
    # Feed the image_data as input to the graph and get first prediction
    softmax_tensor = sess.graph.get_tensor_by_name('final_result:0')
    
    predictions = sess.run(softmax_tensor, {'DecodeJpeg/contents:0': image_data})
    
    # Sorting the classes to show them in the order of increasing accuracy level
    top_k = predictions[0].argsort()[-len(predictions[0]):][::-1]
    
    for node_id in top_k:
        human_string = label_lines[node_id]
        score = predictions[0][node_id]
        print('%s (score = %.5f)' % (human_string, score))
