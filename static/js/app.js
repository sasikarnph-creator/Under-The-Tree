document.addEventListener('DOMContentLoaded', ()=>{
  updateCartCount()

  // Add-to-cart buttons
  document.querySelectorAll('.add-btn').forEach(btn=>{
    btn.addEventListener('click', async e=>{
      const id = btn.dataset.id
      const res = await fetch('/api/add', {method:'POST', headers:{'Content-Type':'application/json'}, body:JSON.stringify({product_id:id})})
      if(res.ok){
        const j = await res.json()
        document.getElementById('cart-count').textContent = j.qty
      }
    })
  })

  // Filter
  document.querySelectorAll('.filter-btn').forEach(b=>{
    b.addEventListener('click', ()=>{
      const cat = b.dataset.cat
      document.querySelectorAll('.product-card').forEach(card=>{
        if(cat==='all' || card.dataset.category===cat) card.style.display = ''
        else card.style.display = 'none'
      })
    })
  })

  // Search (header search & hero)
  const searchInput = document.getElementById('search-input')
  if(searchInput){
    searchInput.addEventListener('input', ()=>{
      const q = searchInput.value.trim().toLowerCase()
      document.querySelectorAll('.product-card').forEach(card=>{
        const title = card.querySelector('.book-title')?.textContent?.toLowerCase() || ''
        const cat = card.dataset.category || ''
        if(!q || title.includes(q) || cat.includes(q)) card.style.display = ''
        else card.style.display = 'none'
      })
    })
  }

  // Cart page: qty change & remove
  document.querySelectorAll('.qty-input').forEach(input=>{
    input.addEventListener('change', async ()=>{
      const id = input.dataset.id
      const qty = input.value
      await fetch('/api/update', {method:'POST', headers:{'Content-Type':'application/json'}, body:JSON.stringify({product_id:id, qty:qty})})
      location.reload()
    })
  })

  document.querySelectorAll('.remove-btn').forEach(b=>{
    b.addEventListener('click', async ()=>{
      const id = b.dataset.id
      await fetch('/api/remove', {method:'POST', headers:{'Content-Type':'application/json'}, body:JSON.stringify({product_id:id})})
      location.reload()
    })
  })

})

async function updateCartCount(){
  try{
    const res = await fetch('/api/cart')
    if(res.ok){
      const j = await res.json()
      document.getElementById('cart-count').textContent = j.qty
    }
  }catch(e){console.warn(e)}
}
