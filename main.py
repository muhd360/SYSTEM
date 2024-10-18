import subprocess
from src import logger
from src.pipeline.preprocessing import PreProcessor
from src.freshness.glcm_config import postprocessor
#defect detection.


#preprocessing stage
STAGE_NAME = "Data Ingestion stage"

try:
   logger.info(f">>>>>> stage {STAGE_NAME} started <<<<<<") 
   image_folder = "/home/muhd/Desktop/GRID/images/box"
   output_folder = "/home/muhd/Desktop/GRID/images/box/box_remove"
   data_ingestion = PreProcessor(image_folder, output_folder)
   data_ingestion.run_background_removal_pipeline()
   logger.info(f">>>>>> stage {STAGE_NAME} completed <<<<<<\n\nx==========x")
except Exception as e:
        logger.exception(e)
        raise e



#database

STAGE_NAME = "Database Connection stage"
try: 
   logger.info(f"*******************")
   logger.info(f">>>>>> stage {STAGE_NAME} started <<<<<<")
   prepare_base_model = PrepareBaseModelTrainingPipeline()
   prepare_base_model.main()
   logger.info(f">>>>>> stage {STAGE_NAME} completed <<<<<<\n\nx==========x")
except Exception as e:
        logger.exception(e)
        raise e

#postprocessing stage

STAGE_NAME = "POSTPROCESSING stage"
try: 
   logger.info(f"*******************")
   logger.info(f">>>>>> stage {STAGE_NAME} started <<<<<<")
   if(db['field'] == 'value'):
      fp=""
      post_processor = postprocessor()
      latest_img=post_processor.get_latest_image("fp")
      post_processor.plot_img(latest_img)

   else if(db['fieldprime'] == 'valueprime'):
      input_img, output_img = "input.jpg", "output.jpg"
      WIDTH,min_def = 100,10
      subprocess.run(["./myprogram2", input_img, output_img, str(WIDTH), str(min_def)])

   logger.info(f">>>>>> stage {STAGE_NAME} completed <<<<<<\n\nx==========x")
except Exception as e:
        logger.exception(e)
        raise e




STAGE_NAME = "Evaluation stage"
try:
   logger.info(f"*******************")
   logger.info(f">>>>>> stage {STAGE_NAME} started <<<<<<")
   model_evalution = EvaluationPipeline()
   model_evalution.main()
   logger.info(f">>>>>> stage {STAGE_NAME} completed <<<<<<\n\nx==========x")

except Exception as e:
        logger.exception(e)
        raise e