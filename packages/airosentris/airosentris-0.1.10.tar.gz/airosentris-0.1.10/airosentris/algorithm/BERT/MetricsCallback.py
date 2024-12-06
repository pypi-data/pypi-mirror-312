import logging
from transformers import TrainerCallback

from airosentris.utils.network_utils import post_data
from airosentris import Config


class MetricsCallback(TrainerCallback):
    def __init__(self, logger, project_id, run_id):
        self.project_id = project_id
        self.run_id = run_id
        self.logger = logger
        self.metrics = []
        self.epoch = 0

    # def on_train_begin(self, args, state, control, **kwargs):
    #     self.logger.log_command(self.project_id, self.run_id, "Training started.")        
    #     self.logger.log_status(self.project_id, self.run_id, "start")

    def on_init_end(self, args, state, control, **kwargs):
        self.epoch = args.num_train_epochs

    def on_epoch_end(self, args, state, control, **kwargs):
        self.logger.log_command(self.project_id, self.run_id, f"Epoch {state.epoch} ended.")

    def on_train_end(self, args, state, control, **kwargs):
        self.logger.log_command(self.project_id, self.run_id, "Training ended.")
        self.logger.log_status(self.project_id, self.run_id, "end")

    def on_evaluate(self, args, state, control, **kwargs):        
        self.logger.log_command(self.project_id, self.run_id, f"Evaluation started for step {state.global_step}.")
        print("Total Epoch:", args.num_train_epochs)
        print("Jumlah log:", len(state.log_history))
        if len(state.log_history) <= args.num_train_epochs: #fix soon
            metrics = state.log_history[-1]             
            metrics_message = {
                "epoch": int(metrics["epoch"]),
                "accuracy": round(metrics["eval_accuracy"]["accuracy"], 2),
                "f1_score": round(metrics["eval_f1"]["f1"], 2),
                "precision": round(metrics["eval_precision"]["precision"], 2),
                "recall": round(metrics["eval_recall"]["recall"], 2),
                "loss": round(metrics["eval_loss"], 2),
                "runtime": round(metrics["eval_runtime"], 2),
                "samples_per_second": round(metrics["eval_samples_per_second"], 2),
                "steps_per_second": round(metrics["eval_steps_per_second"], 2),
                "step": int(metrics["step"])
            }

            self.logger.log_metric(self.project_id, self.run_id, metrics_message)

            metrics_data = {
                "run_id" : self.run_id,
                "epoch": int(metrics["epoch"]),
                "accuracy": round(metrics["eval_accuracy"]["accuracy"], 2),
                "f1_score": round(metrics["eval_f1"]["f1"], 2),
                "precision": round(metrics["eval_precision"]["precision"], 2),
                "recall": round(metrics["eval_recall"]["recall"], 2),
            }

            MetricsCallback.send_metric_log(metrics_data)

    @staticmethod
    def send_metric_log(log):
        endpoint = "api/v1/run/log"
        try:
            logging.info(f"Sending metrics to API: {log}")
            response = post_data(endpoint=endpoint, data=log)
            logging.info(f"Metrics sent to API: {response.json()}")
            return response
        except Exception as e:
            logging.error(f"Failed to send metrics to API: {e}")