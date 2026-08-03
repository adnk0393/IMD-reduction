require(ggplot2)
require(RColorBrewer)
require(ggtern)
require(ggrastr)

rm(list = ls())
gc() 

setwd("C:/Users/naik3/Documents/Research/Mineral identifier ann IISER Mohali/new computational scripts")

normalize <- function(data) {
  sm <- rowSums(data)
  data <- data * 100 / sm
  data <- round(data,2)
  return(data)
}

make_femgmn_tern <- function(data){
  data = data[c("FeO","MnO","MgO")]
  data = normalize(data)
  data = as.data.frame(data)
  return(data)
}

plot_grt_confidence_ternary <- function(training_data, grt_prediction_data, misclass_data = NULL, colorbar = FALSE) {
  dpi = 1200
  training_data <- training_data[training_data$Mineral == "Grt",]
  grt_train <- make_femgmn_tern(training_data)
  if (!is.null(misclass_data)) {
    misclass_data = misclass_data[misclass_data$Mineral == "Grt",]
    misclass_data = make_femgmn_tern(misclass_data)
  }
  predData = make_femgmn_tern(grt_prediction_data)
  predData["Confidence"] = grt_prediction_data["Grt"]
  predData[predData["Confidence"] < 0.5, "Confidence"] <- 0
  predData[predData["Confidence"] >= 0.5, "Confidence"] <- 1
  predData["Mineral"] = grt_prediction_data$PredMin
  
  fig = ggtern(data = predData, aes(x = FeO, y = MnO, z = MgO)) + 
    rasterise(geom_point(aes(colour = Confidence), shape = 15), dpi = dpi) + 
    # scale_color_gradient(low = "darkgray", high = "white", guide = colorbar, breaks = seq(0,1,0.05), limits = c(0,1)) +
    scale_color_gradient(low = "#A9A9A9", high = "#FFFFFFFF", guide = colorbar, limits = c(0,1)) +
    rasterise(geom_point(data = grt_train, aes(x = FeO, y = MnO, z = MgO), size = 0.05), dpi = dpi) +
    theme_classic()
  if (!is.null(misclass_data)) {
    fig = fig + geom_point(data = misclass_data, aes(x = FeO, y = MnO, z = MgO), shape = 17, size = 5, colour = "red")
  }
  return(fig)
}

model = "RF"
grt_c1 = paste0("Grt_prediction_for_",model,"_C1.csv")
grt_c4 = paste0("Grt_prediction_for_",model,"_C4.csv")
grt_c3 = paste0("Grt_prediction_for_",model,"_C3.csv")
mis_val_data_c1 <- paste0("KNN eval/Misclassified_data_from_", model,"_C1_on_validation_data.csv" )
mis_val_data_c3 <- paste0("KNN eval/Misclassified_data_from_", model,"_C3_on_validation_data.csv" )
mis_val_data_c4 <- paste0("KNN eval/Misclassified_data_from_", model,"_C4_on_validation_data.csv" )
output = paste0("diagrams/Grt_prediction_confidence_",model,".pdf")

training_data <- read.csv("KNN eval/Training data.csv", header = 1)
misclassified_data_c1 <- read.csv(mis_val_data_c1, header = 1)
misclassified_data_c3 <- read.csv(mis_val_data_c3, header = 1)
misclassified_data_c4 <- read.csv(mis_val_data_c4, header = 1)

grt_prediction_data <- read.csv(grt_c1)
fig_c1 = plot_grt_confidence_ternary(training_data, grt_prediction_data)
fig1_c1 = ggplotGrob(fig_c1)

grt_prediction_data <- read.csv(grt_c4)
fig_c4 = plot_grt_confidence_ternary(training_data, grt_prediction_data)
fig1_c4 = ggplotGrob(fig_c4)

grt_prediction_data <- read.csv(grt_c3)
fig_c3 = plot_grt_confidence_ternary(training_data, grt_prediction_data)
fig1_c3 = ggplotGrob(fig_c3)

require(cowplot)
plot_grid(fig1_c1,fig1_c4,fig1_c3, ncol = 3, labels = c("C1", "C4", "C3"))
ggsave(output, device = "pdf")
gc()