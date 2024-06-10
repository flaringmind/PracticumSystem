import react from "react"
import { BrowserRouter, Routes, Route, Navigate } from "react-router-dom"
import Login from "./pages/Login"
import Register from "./pages/Register"
import Home from "./pages/Home"
import CreateDataset from "./pages/CreateDataset"
import DatasetPage from "./pages/DatasetPage"
import NotFound from "./pages/NotFound"
import ProtectedRoute from "./components/ProtectedRoute"
import "./styles/App.css"

function Logout() {
  localStorage.clear()
  return <Navigate to="/login" />
}

function RegisterAndLogout() {
  localStorage.clear()
  return <Register />
}

function App() {

  return (
    <BrowserRouter>
      <Routes>
        <Route path="/" element={<ProtectedRoute><Home /></ProtectedRoute>}/>
        <Route path="/create" element={<ProtectedRoute><CreateDataset /></ProtectedRoute>}/>
        <Route path="/dataset/:id" element={<ProtectedRoute><DatasetPage /></ProtectedRoute>}/>
        <Route path="/login" element={<Login />} />
        <Route path="/logout" element={<Logout />} />
        <Route path="/register" element={<RegisterAndLogout />} />
        <Route path="*" element={<NotFound />} />
      </Routes>
    </BrowserRouter>
  )
}

export default App