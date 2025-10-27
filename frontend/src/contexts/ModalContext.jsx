import { createContext, useContext, useState } from 'react'

const ModalContext = createContext()

export function ModalProvider({ children }) {
  const [modalState, setModalState] = useState({
    isOpen: false,
    plant: null
  })

  const openModal = (plant) => {
    setModalState({
      isOpen: true,
      plant
    })
  }

  const closeModal = () => {
    setModalState({
      isOpen: false,
      plant: null
    })
  }

  return (
    <ModalContext.Provider value={{ modalState, openModal, closeModal }}>
      {children}
    </ModalContext.Provider>
  )
}

export function useModal() {
  const context = useContext(ModalContext)
  if (!context) {
    throw new Error('useModal must be used within a ModalProvider')
  }
  return context
}