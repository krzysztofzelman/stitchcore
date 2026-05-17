import { useEffect, useState } from 'react'
import {
  Typography, Paper, Table, TableBody, TableCell, TableContainer,
  TableHead, TableRow, Button, Dialog, DialogTitle, DialogContent,
  TextField, Box, Alert, Tab, Tabs, Select, MenuItem, Chip,
} from '@mui/material'
import { inventoryApi, productsApi } from '../api/client'

interface StockItem {
  id: number
  variant_id: number
  location_id: number
  quantity: number
  reserved_quantity: number
  low_stock_threshold: number
  location_code: string | null
}

interface Location {
  id: number
  code: string
  zone: string
  aisle: string
  rack: string
  shelf: string
  description?: string
  is_active: boolean
}

interface Movement {
  id: number
  variant_id: number
  movement_type: string
  quantity: number
  reference: string
  notes: string
  created_at: string
}

export default function Inventory() {
  const [tab, setTab] = useState(0)
  const [stock, setStock] = useState<StockItem[]>([])
  const [locations, setLocations] = useState<Location[]>([])
  const [movements, setMovements] = useState<Movement[]>([])
  const [adjustDialog, setAdjustDialog] = useState(false)
  const [locationDialog, setLocationDialog] = useState(false)
  const [adjustForm, setAdjustForm] = useState({ variant_id: 0, location_id: 0, quantity: 0, notes: '' })
  const [locForm, setLocForm] = useState({ code: '', zone: '', aisle: '', rack: '', shelf: '', description: '' })
  const [message, setMessage] = useState('')

  const loadData = () => {
    inventoryApi.stock().then(({ data }) => setStock(data || []))
    inventoryApi.locations().then(({ data }) => setLocations(data || []))
    inventoryApi.movements({ page_size: 50 }).then(({ data }) => setMovements(data.results || []))
  }

  useEffect(loadData, [])

  const handleAdjust = async () => {
    try {
      await inventoryApi.adjust(adjustForm)
      setMessage('Stan zaktualizowany')
      setAdjustDialog(false)
      loadData()
    } catch (err: any) {
      setMessage('Błąd: ' + (err.response?.data?.detail || 'nieznany'))
    }
  }

  const handleCreateLocation = async () => {
    try {
      await inventoryApi.createLocation(locForm)
      setMessage('Lokalizacja utworzona')
      setLocationDialog(false)
      loadData()
    } catch (err: any) {
      setMessage('Błąd: ' + (err.response?.data?.detail || 'nieznany'))
    }
  }

  return (
    <div>
      <Typography variant="h4" fontWeight={700} mb={2}>Magazyn</Typography>
      {message && <Alert severity={message.startsWith('Błąd') ? 'error' : 'success'} sx={{ mb: 2 }} onClose={() => setMessage('')}>{message}</Alert>}

      <Box display="flex" gap={2} mb={2}>
        <Button variant="contained" onClick={() => setAdjustDialog(true)}>Koryguj stan</Button>
        <Button variant="outlined" onClick={() => setLocationDialog(true)}>Nowa lokalizacja</Button>
      </Box>

      <Tabs value={tab} onChange={(_, v) => setTab(v)} sx={{ mb: 2 }}>
        <Tab label="Stan magazynowy" />
        <Tab label="Lokalizacje" />
        <Tab label="Ruchy" />
      </Tabs>

      {tab === 0 && (
        <TableContainer component={Paper}>
          <Table size="small">
            <TableHead>
              <TableRow>
                <TableCell>Variant ID</TableCell>
                <TableCell>Lokalizacja</TableCell>
                <TableCell align="right">Ilość</TableCell>
                <TableCell align="right">Zarezerwowane</TableCell>
                <TableCell align="right">Dostępne</TableCell>
                <TableCell>Próg</TableCell>
              </TableRow>
            </TableHead>
            <TableBody>
              {stock.map((s) => (
                <TableRow key={s.id} sx={s.quantity <= s.low_stock_threshold ? { bgcolor: '#fef2f2' } : {}}>
                  <TableCell>{s.variant_id}</TableCell>
                  <TableCell>{s.location_code || '-'}</TableCell>
                  <TableCell align="right">{s.quantity}</TableCell>
                  <TableCell align="right">{s.reserved_quantity}</TableCell>
                  <TableCell align="right">{s.quantity - s.reserved_quantity}</TableCell>
                  <TableCell>{s.quantity <= s.low_stock_threshold && <Chip label="Niski stan" size="small" color="error" />}</TableCell>
                </TableRow>
              ))}
            </TableBody>
          </Table>
        </TableContainer>
      )}

      {tab === 1 && (
        <TableContainer component={Paper}>
          <Table size="small">
            <TableHead>
              <TableRow>
                <TableCell>Kod</TableCell>
                <TableCell>Strefa</TableCell>
                <TableCell>Aleja</TableCell>
                <TableCell>Regał</TableCell>
                <TableCell>Półka</TableCell>
                <TableCell>Opis</TableCell>
              </TableRow>
            </TableHead>
            <TableBody>
              {locations.map((l) => (
                <TableRow key={l.id}>
                  <TableCell>{l.code}</TableCell>
                  <TableCell>{l.zone}</TableCell>
                  <TableCell>{l.aisle}</TableCell>
                  <TableCell>{l.rack}</TableCell>
                  <TableCell>{l.shelf}</TableCell>
                  <TableCell>{l.description}</TableCell>
                </TableRow>
              ))}
            </TableBody>
          </Table>
        </TableContainer>
      )}

      {tab === 2 && (
        <TableContainer component={Paper}>
          <Table size="small">
            <TableHead>
              <TableRow>
                <TableCell>Variant</TableCell>
                <TableCell>Typ</TableCell>
                <TableCell align="right">Ilość</TableCell>
                <TableCell>Referencja</TableCell>
                <TableCell>Uwagi</TableCell>
                <TableCell>Data</TableCell>
              </TableRow>
            </TableHead>
            <TableBody>
              {movements.map((m) => (
                <TableRow key={m.id}>
                  <TableCell>{m.variant_id}</TableCell>
                  <TableCell>{m.movement_type}</TableCell>
                  <TableCell align="right">{m.quantity}</TableCell>
                  <TableCell>{m.reference}</TableCell>
                  <TableCell>{m.notes}</TableCell>
                  <TableCell>{new Date(m.created_at).toLocaleDateString('pl-PL')}</TableCell>
                </TableRow>
              ))}
            </TableBody>
          </Table>
        </TableContainer>
      )}

      {/* Adjust dialog */}
      <Dialog open={adjustDialog} onClose={() => setAdjustDialog(false)}>
        <DialogTitle>Korekta stanu</DialogTitle>
        <DialogContent>
          <TextField label="Variant ID" type="number" fullWidth sx={{ mb: 2, mt: 1 }}
            value={adjustForm.variant_id} onChange={(e) => setAdjustForm({ ...adjustForm, variant_id: Number(e.target.value) })} />
          <TextField label="Location ID" type="number" fullWidth sx={{ mb: 2 }}
            value={adjustForm.location_id} onChange={(e) => setAdjustForm({ ...adjustForm, location_id: Number(e.target.value) })} />
          <TextField label="Ilość (+/-)" type="number" fullWidth sx={{ mb: 2 }}
            value={adjustForm.quantity} onChange={(e) => setAdjustForm({ ...adjustForm, quantity: Number(e.target.value) })} />
          <TextField label="Uwagi" fullWidth multiline rows={2}
            value={adjustForm.notes} onChange={(e) => setAdjustForm({ ...adjustForm, notes: e.target.value })} />
        </DialogContent>
        <Box sx={{ p: 2, display: 'flex', gap: 1, justifyContent: 'flex-end' }}>
          <Button onClick={() => setAdjustDialog(false)}>Anuluj</Button>
          <Button variant="contained" onClick={handleAdjust}>Zapisz</Button>
        </Box>
      </Dialog>

      {/* Location dialog */}
      <Dialog open={locationDialog} onClose={() => setLocationDialog(false)}>
        <DialogTitle>Nowa lokalizacja</DialogTitle>
        <DialogContent>
          <TextField label="Kod" fullWidth sx={{ mb: 2, mt: 1 }} value={locForm.code}
            onChange={(e) => setLocForm({ ...locForm, code: e.target.value })} />
          <TextField label="Strefa" fullWidth sx={{ mb: 2 }} value={locForm.zone}
            onChange={(e) => setLocForm({ ...locForm, zone: e.target.value })} />
          <TextField label="Aleja" fullWidth sx={{ mb: 2 }} value={locForm.aisle}
            onChange={(e) => setLocForm({ ...locForm, aisle: e.target.value })} />
          <TextField label="Regał" fullWidth sx={{ mb: 2 }} value={locForm.rack}
            onChange={(e) => setLocForm({ ...locForm, rack: e.target.value })} />
          <TextField label="Półka" fullWidth sx={{ mb: 2 }} value={locForm.shelf}
            onChange={(e) => setLocForm({ ...locForm, shelf: e.target.value })} />
          <TextField label="Opis" fullWidth value={locForm.description}
            onChange={(e) => setLocForm({ ...locForm, description: e.target.value })} />
        </DialogContent>
        <Box sx={{ p: 2, display: 'flex', gap: 1, justifyContent: 'flex-end' }}>
          <Button onClick={() => setLocationDialog(false)}>Anuluj</Button>
          <Button variant="contained" onClick={handleCreateLocation}>Utwórz</Button>
        </Box>
      </Dialog>
    </div>
  )
}
