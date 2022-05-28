# CodeNote

Code notes by CYY. 



## Demo

The ```demo/main.py``` file run the ```GraspEstimator```, which is the sampler+evaluator on the demo data.

It merely turn the depth data into the camera-frame point-cloud and then run the estimator on it. 

Need to figure out the network input and output format. The process is in the ```GraspEstimator.generate_and_refine_grasps``` function.

- [x] Input (generator)
  - [x] The input format of the network? (N, 3) point cloud
  - [x] Object only or the entire observed scene? - Object only. Confirmed from the paper and the code
  - [x] Preprocess? - in the preprocess-pc function
    - Downsample to get limited amount of points (1024). **Again can PointNet++  process larget amount of points?**
    - Centralize - Subtract object mean
    - 
- [x] Output (generator)
  - [x] The output format of the grasps?
    - The format is a 4-by-4 matrix accepted by the ```trimesh.mesh.apply_transform```. So it is the homogeneous frame transformation matrix.
  - [x] In what frame? - Object frame
  - [x] Postprocess ? 
    - Decentralize - Add back the object point cloud mean. In the ```utils.denormalize_grasps``` function



## Train

The main training class is the ``` grasp_net.GraspNetModel```. 

The required inputs, as in the ```GraspNetModel.set_inputs``` method, are:

- ```pc```: The point cloud. **Note: It duplicate the object point cloud to have the shape (*N_gpo*, N_obj_pc, 3)**
  - [x] In which frame? High chance is camera. Confirmed!
  - [ ] Content. Only the object or object + table? - Object only
  - [x] Preprocess from the dataloader side? Some in the ```change_object_and_render``` functtion
    - ```apply_dropout``` - Seem to drop some points, but not applied given the parameter setting
    - Get fixed point number (1024)
    - Centeralize 
  
- ```grasp_rt```: The ground truth grasps (positive).
  - [x] What is the format?  (*N_gpo*, 16), where 16 is the vectorized homogeneous transformation matrix
    -  It's set to have a fixed number of grasps/object *N_gpo = 64*. If the number of the grasp cluster is smaller than that number, then sample with put back.
  - [x] Relate to what frame? Camera
  
  - [x] Need preprocess?  Seems not. Just get the camera frame is okay.
  
- ```target_cps```: This is the control points used to calculate the reconstruction error.
  - [x] ```utils.transform_control_points_numpy``` can get the points given the grasp poses.
  
- There are others that seem not used in the training process:

  - [ ] ```pc_pose```: The object pose in the camera frame. (inverse of the camera pose)
  - [ ] ```cad_path```
  - [ ] ```cad_scale```
  - [ ] ```quality```