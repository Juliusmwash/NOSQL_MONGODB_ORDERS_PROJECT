document.addEventListener("DOMContentLoaded", function() {
    const searchDivs = document.querySelectorAll('.child-div');
    const sortDivs = document.querySelectorAll('.child-div2');
    const inputElements = document.querySelectorAll('.class-input');
    const shopNameInput = document.getElementById('shop-name');
    const dateInput = document.getElementById('date');
    const email = document.getElementById('email');
    const hiddenNoEmail = document.getElementById('hidden_no_email');
    const hiddenSearchInput = document.getElementById('hidden-search-input');
    const hiddenSortInput = document.getElementById('hidden-sort-input');
    const hiddenPureShopnameInput = document.getElementById('hidden-pure-shopname-input');
    const buttons = document.querySelectorAll('.button');
    const scrollableDiv = document.querySelector('.scrollable-div');
    const selectDisplay = document.getElementById('select-display');
    const selectDisplay2 = document.getElementById('select-display2');
    const selectDisplay3 = document.getElementById('select-display3');

    // Variable to hold the total price as the orders are being shown
    let grandTotalPrice = 0;

    // Variables to keep page tracks
    let pageNumber = 0;
    let previousPage = 0;
    let strictPageNumber = 0;

    // Array to keep track of the real calculations as they happen
    let priceArray = [];
  

    inputElements.forEach((element) => {
        element.addEventListener('input', () => {
            grandTotalPrice = 0;
        });
    });

    searchDivs.forEach((element, index) => {
        element.addEventListener('click', () => {
            grandTotalPrice = 0;
            if (index === 0) {
                hiddenSearchInput.value = 'shopname';
                selectDisplay.textContent = element.textContent;
            } else if (index === 1) {
                hiddenSearchInput.value = 'date';
                selectDisplay.textContent = element.textContent;
            } else if (index === 2) {
                hiddenSearchInput.value = 'both';
                selectDisplay.textContent = element.textContent;
            } else if (index === 3) {
                hiddenSearchInput.value = 'email';
                selectDisplay3.textContent = element.textContent;
            } else if (index === 4) {
                hiddenPureShopnameInput.value = '5';
                selectDisplay3.textContent = element.textContent;
            } else if (index === 5) {
                hiddenNoEmail.value = 1;
                selectDisplay3.textContent += ` / ${element.textContent}`;
            }
        });
    });

    sortDivs.forEach((element, index) => {
        element.addEventListener('click', () => {
            if (index === 0) {
                hiddenSortInput.value = 1;
                selectDisplay2.textContent = element.textContent;
            } else if (index === 1) {
                hiddenSortInput.value = -1;
                selectDisplay2.textContent = element.textContent;
            }
        });
    });

    buttons.forEach((element) => {
        element.addEventListener('click', () => {
            element.style.backgroundColor = 'cyan';
            pageNumber = parseInt(element.textContent);
            let check = true;

            const num = parseInt(element.textContent);
            const skip = (num - 1) * 20;

            // Define base URL
            const baseUrl = "/fetch_orders";

            // Create an object to hold the parameters
            let params = new URLSearchParams();

            // Add parameters to the object
            if (hiddenSearchInput.value === 'shopname') {
                if (!shopNameInput.value) {
                    shopNameInput.focus();
                    check = false;
                }
                params.append("shop_name", shopNameInput.value);
                if (hiddenSortInput.value) {
                    params.append("sort_order", hiddenSortInput.value);
                } else {
                    params.append("sort_order", -1);
                }
            } else if (hiddenSearchInput.value === 'date') {
                if (!dateInput.value) {
                    dateInput.focus();
                }
                params.append("date", dateInput.value);
                if (hiddenSortInput.value) {
                    params.append("sort_order", hiddenSortInput.value);
                } else {
                    params.append("sort_order", -1);
                }
            } else if (hiddenSearchInput.value === 'both') {
                if (!shopNameInput.value) {
                    shopNameInput.focus();
                }
                if (!dateInput.value) {
                    dateInput.focus();
                    check = false;
                }
                params.append("shop_name", shopNameInput.value);
                params.append("date", dateInput.value);
                if (hiddenSortInput.value) {
                    params.append("sort_order", hiddenSortInput.value);
                } else {
                    params.append("sort_order", -1);
                }
            } else if (hiddenSearchInput.value === 'email') {
                if (!email.value) {
                    email.focus();
                    check = false;
                }
                params.append("email", email.value);
                if (hiddenSortInput.value) {
                    params.append("sort_order", hiddenSortInput.value);
                } else {
                    params.append("sort_order", -1);
                }
            } else {
              if (hiddenSortInput.value) {
                params.append("sort_order", hiddenSortInput.value);
              } else {
                params.append("sort_order", -1);
              }
            }

            // Construct the full URL with parameters
            if (hiddenPureShopnameInput.value && hiddenPureShopnameInput.value === "5") {
                params = new URLSearchParams();
                if (!shopNameInput.value) {
                    shopNameInput.focus();
                    check = false;
                }
                params.append("pure_shop", shopNameInput.value);
                params.append("sort_order", -1);
            }
            if (hiddenNoEmail.value) {
                params.append("no_email", "no_email");
            }
            params.append("skip", skip);






          if (check) {
            const fullUrl = `${baseUrl}?${params.toString()}`;
            //alert(`fullUrl = ${fullUrl}`);

            // Send a GET request and update the div when the response is received
            fetch(fullUrl)
              .then(response => {
                if (!response.ok) {
                  throw new Error('Network response was not ok');
                }
                return response.json();
              })
              .then(data => {
                // Access objects from the 'order' key
                const orderObjects = data.map(item => item.order);
                const num = orderObjects.length;
                if (orderObjects.length > 0) {
                  grandTotalPrice = parseFloat(grandTotalPrice);
                  let tempTotalPrice = 0;

                  let ordersHTML = ordersCountElementsGenerator(num, pageNumber);

                  for (let i = 0; i < orderObjects.length; i++) {
                    const obj = orderObjects[i];
                    obj['order_count'] = i + 1;
                    tempTotalPrice += parseFloat(obj.total_price);
                    ordersHTML += divElementsGenerator(obj);
                  }
                  //alert(`price array length = ${priceArray.length}`);

                  // Reverse grand total calculations
                  if (pageNumber <= previousPage && previousPage !== 0) {
                    let reducePrice = 0;
                    for (let i = pageNumber; i < priceArray.length; i++) {
                      reducePrice += priceArray[i];
                      //alert(`reducePrice = ${reducePrice}`);
                    }
                    priceArray.splice(pageNumber);
                    grandTotalPrice = parseFloat(grandTotalPrice - reducePrice).toFixed(2);
                    previousPage = pageNumber - 1;
                    //alert("decremented");
                  } else if (pageNumber > previousPage && strictPageNumber != pageNumber) {
                  priceArray.push(tempTotalPrice);
                  grandTotalPrice = parseFloat((grandTotalPrice + tempTotalPrice)).toFixed(2);
                  previousPage = pageNumber;
                  }
                  strictPageNumber = pageNumber;

                  ordersHTML += totalPriceElements(grandTotalPrice);
                  // Update the div's innerHTML
                  scrollableDiv.innerHTML = ordersHTML;
                } else {
                  scrollableDiv.innerHTML = `<p style="font-size: 18px; color: #FF0000;" id="zmc-tv">No orders match the requested field(s), or, all orders have already been shown.</p>`;
                }
              })
              .catch(error => {
                console.error('Error:', error);
                alert(`Error: ${error}`);
              });
          }
        });
    });

    function ordersCountElementsGenerator(orderCount, pageNumber) {
        return `
            <div class="order-page-count">
                <span class="page-count">Pg. ${pageNumber}</span>
                <span class="order-count">${orderCount} Orders</span>
            </div>
        `;
    }

    function divElementsGenerator(obj) {
        return `
            <div class="order-box">
              <span class="show-order-count">${obj.order_count}</span>
                <div class="header-one">
                    <span class="span-row">Shop Name</span>
                    <span class="span-row">Item Type</span>
                    <span class="span-row">Price</span>
                    <span class="span-row">Quantity</span>
                    <span class="span-row">Total Price</span>
                    <span class="span-row">Date & Time</span>
                    <span class="span-row">Email</span>
                    <span class="span-row">Order Id</span>
                </div>
                <div class="header-two">
                    <span class="span-row2">${obj.shop_name}</span>
                    <span class="span-row2">${obj.item_type}</span>
                    <span class="span-row2">Ksh. ${obj.price_kg} &ensp;/kg</span>
                    <span class="span-row2">${obj.quantity}</span>
                    <span class="span-row2">Ksh. ${obj.total_price}</span>
                    <span class="span-row2">${obj.date_time}</span>
                    <span class="span-row2">${obj.ser_sort[0]}</span>
                    <span class="span-row2" style="font-size: 9px;">${obj.order_id}</span>
                </div>
            </div>
        `;
    }

    function totalPriceElements(ttlPrc) {
      const strTtlPrc = String(ttlPrc)
      let newTtlPrc = '';

      if (strTtlPrc.length === 8) {
        for (let i = 0; i < 8; i++) {
          if (i === 2) {
            newTtlPrc += ',';
          }
          newTtlPrc += strTtlPrc[i];
        }
      } else if (strTtlPrc.length === 9) {
        for (let i = 0; i < 9; i++) {
          if (i === 3) {
            newTtlPrc += ',';
          }
          newTtlPrc += strTtlPrc[i];
        }
      } else {
        newTtlPrc = String(ttlPrc);
      }
        return `
            <div class="total-price" style="width: 100%; height: 40px; padding: 0 10px; display: flex; justify-content: center; align-items: center; color: orange; font-size: 18px; font-weight: bold; border: 2px solid lime;/*#00c6ff;*/ border-radius: 10px; margin-bottom: 50px;">
                <span class="total-price-header" style="margin-right: 10px; color: #ddd6f3;">GRAND TOTAL</span>
                <span class="total-price-value" style="color: #20BDFF;/*#D11FFBD;*/ font-size: 20px;">Ksh. ${newTtlPrc}</span>
            </div>
        `;
    }
});

