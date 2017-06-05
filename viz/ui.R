
library(shiny)
library(leaflet)
library(shinythemes)

navbarPage(theme = shinytheme('flatly'),
  "Events in New York", id='nav',
           tabPanel("Evens in NY",
                    
                    div(class = 'outer',
                        tags$head(
                          includeCSS("styles.css")
                        ),
                        leafletOutput("map", width = "100%", height = "100%"),
                        absolutePanel(id = "controls", class = "panel panel-default", fixed = TRUE,
                                      draggable = TRUE, top = 600, left = "auto", right = 40, bottom = "auto",
                                      width = 400, height = 200,
                                      h2("Instagram Posts in NY"),
                                      sliderInput('time_range', 'choose date range:',min = as.POSIXct('2012-11-30 15:50:10'), 
                                                  max = as.POSIXct('2014-02-24 20:07:50'),
                                                  value = c(as.POSIXct('2014-01-01 00:00:00'), as.POSIXct('2014-02-24 20:07:50')),
                                                  timeFormat = "%F %T")
                                      ))),
          tabPanel("Evens in NY - Animation",
                   div(class = 'outer',
                    tags$head(
                      includeCSS("styles.css")
               ),
               leafletOutput("map_ani", width = "100%", height = "100%"),
               absolutePanel(id = "controls", class = "panel panel-default", fixed = TRUE,
                             draggable = TRUE, top = 600, left = "auto", right = 40, bottom = "auto",
                             width = 400, height = 200,
                             h2("Instagram Posts in NY"),
                             
                             sliderInput('time_point', 'time point:',min = as.POSIXct('2013-05-03 08:50:10'), 
                                                  max = as.POSIXct('2014-02-24 20:07:50'),
                                                  value = c(as.POSIXct('2014-01-12 00:00:00')),
                                                  timeFormat = "%F %T", step = 1000000,
                                         animate = animationOptions(interval = 1700, loop = TRUE, playButton='play',pauseButton='pause'))
                                      ))
                    
                    )
)
           
