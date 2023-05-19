import './App.css';
import { Line } from 'react-chartjs-2'
import {
  Chart,
  LineElement,
  CategoryScale, //x axis
  LinearScale, //y axis
  PointElement
} from "chart.js"
import { db } from './firebase.js'
import { ref, onValue } from 'firebase/database'
import { useState, useEffect } from 'react'


Chart.register(
  LineElement,
  CategoryScale,
  LinearScale, 
  PointElement
)

const App = () => {

  // set the variables with usestate()
  const [name, setName] = useState()
  const [times, setTimes] = useState()
  const [labels, setLabels] = useState()
  const [avg, setAvg] = useState()
  const [fStart, setFStart] = useState()


  // use effect loop to get the data frequently so it can detect when it is changed
  useEffect(() => {
    return onValue(ref(db, '/finalproject/'), querySnapshot => {
      // full data snapshot
      let data = querySnapshot.val()
      // graph to be shown on app
      let selectedGraph = data['selectedGraph']
      // get the data for the person who's graph was selected
      let selectedData = data['name'][selectedGraph]
      // get average
      let average = selectedData.average
      // get false starts
      let falseStart = selectedData.false_start
      // get the values of the reaction time key value pairs 
      let reactionTimes = Object.values(selectedData.reaction_time)

      // create labels for each of the reaction time values
      let label = []
      for(let i = 0; i <  reactionTimes.length; i++) {
        label.push("Trial " + (i + 1))
      }

      // set variables
      setTimes(reactionTimes)
      setName(selectedGraph)
      setAvg(average)
      setFStart(falseStart)
      setLabels(label)

    })
  })

  // data for the graph
  const data = {
    labels: labels,
    datasets: [{
      labels: labels,
      data: times,
      backgroundColor: 'aqua',
      borderColor: 'black',
      pointBorderColor: true,
    }]
  }

  // graph options
  const options = {
    plugins: {
      legend: true
    },
    scales: {
      y: {
        min:100,
        max: 800
      }
    }
  }
  
  // graph / stuff on page
  return (
    <div className="App">
        <div style={{
          width: '600px',
          height: '300px',
          padding:'30px'
        }}>
        <h2>{name}'s Reaction Time</h2>
        <Line
          data = {data}
          options = {options}
        ></Line>
        <h3>Average Reaction Time: {avg}</h3>
        <h3>Number of false starts: {fStart}</h3>

        </div>

    </div>
  );
}

export default App;


