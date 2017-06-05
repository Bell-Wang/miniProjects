library(shiny)
library(leaflet)

shinyServer(function(input, output) {

  
  dataInput <- reactive({
    viz_df[which(viz_df$created_time<=input$time_range[2] & viz_df$created_time>=input$time_range[1]),]
  })
  
  output$map <- renderLeaflet({
    leaflet() %>%
      addTiles() %>%
      setView(lng = -74.00, lat = 40.70, zoom = 12) %>%
      addMarkers(lng = dataInput()$mid_lng, lat = dataInput()$mid_lat,
                 popup = as.character(dataInput()$text), clusterOptions=markerClusterOptions())
  })
  
  dataInput_ani <- reactive({
    viz_df[which(viz_df$created_time <= input$time_point+86400*7 & viz_df$created_time >= input$time_point-86400*7),]
  })
  
  output$map_ani <- renderLeaflet({
    
    post_icon <- makeIcon(
      iconUrl = 'http://iconshow.me/media/images/Application/Modern-Flat-style-Icons/png/512/Chat.png',
      iconWidth = 30, iconHeight = 30)
    
    leaflet() %>%
      addTiles() %>%
      setView(lng = -73.90, lat = 40.75, zoom = 12) %>%
      addMarkers(lng = dataInput_ani()$mid_lng, lat = dataInput_ani()$mid_lat,
                 icon= post_icon)
  })
})