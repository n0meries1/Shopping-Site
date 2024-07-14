document.addEventListener('DOMContentLoaded', function() {
    const OpenModalButton = document.getElementById('OpenModalButton');
    const WatchModal = document.getElementById('WatchModal');
    const CloseSpan = document.getElementsByClassName('close')[0];
    const addForm = document.getElementById('addForm');
    const editForm = document.getElementById('editForm');
    const actionSelector = document.getElementById('actionSelector');
    const WatchSelect = document.getElementById('Edit_Watch_Select');
    const dropDownBatchDelete = document.getElementById('dropdown-batch-delete');
    const batchDeleteContainer = document.getElementById('batch-delete-container');
    const updateButton = document.getElementById('edit_submit');
    const toggleCheckboxes = document.querySelectorAll('.checkbox');
    const checkallbox = document.querySelector('.checkallbox-input');


    OpenModalButton.addEventListener('click', () => {
        WatchModal.style.display = 'block';
        addForm.style.display = 'block';
        editForm.style.display = 'none';
    });

    CloseSpan.addEventListener('click', () => {
        WatchModal.style.display = 'none'
    });

    window.addEventListener('click', (event) => {
        if (event.target === WatchModal) {
            WatchModal.style.display = 'none'
        }
    });




    actionSelector.addEventListener('change', (event) => {
        if (event.target.value === 'add') {
            addForm.style.display = 'block';
            editForm.style.display = 'none';
        } 
        
        if (event.target.value === 'edit'){
            addForm.style.display = 'none';
            editForm.style.display = 'block';
            populateWatchSelector();
        }
    });

    async function populateWatchSelector()
    {
        const response = await fetch('/get_watch_name');
        const rawData = await response.text();
        const watches = JSON.parse(rawData);
        WatchSelect.innerHTML = '';
        watches.forEach(watch => {
            const option = document.createElement('option');
            option.value = watch.watch_id;
            option.textContent = watch.watch_name;
            WatchSelect.appendChild(option);
        });

        if (watches.length > 0) {
            WatchSelect.value = watches[0].watch_id;
            populateEditForm(watches[0].watch_id);
        }
    };

    WatchSelect.addEventListener('change', async (event) => {
        const WatchID = event.target.value;
        populateEditForm(WatchID);
    });

    async function populateEditForm(watch_id) 
    {
        const response = await fetch(`/get_watch/${watch_id}`);
        const watch = await response.json();
        document.getElementById('Edit_Watch_Name').value = watch.watch_name;
        document.getElementById('Edit_Watch_Quantity').value = watch.watch_quantity;
        document.getElementById('Edit_Watch_Price').value = watch.watch_price;
        document.getElementById('Edit_Watch_Detail').value = watch.watch_detail;
        document.getElementById('Edit_Watch_Image').value = watch.watch_image;
    }
    
    dropDownBatchDelete.addEventListener('click', () =>
    {
        event.preventDefault();
        batchDeleteContainer.classList.toggle('show');
        if (batchDeleteContainer.classList.contains('show'))
        {
            dropDownBatchDelete.textContent = "Hide Products";
            batchDeleteContainer.style.maxHeight = batchDeleteContainer.scrollHeight + "px";
        }
        else
        {
            dropDownBatchDelete.textContent = "Show Products";
        }
    });

    updateButton.addEventListener('click', () => {
        const selectedCheckboxes = document.querySelectorAll('.checkbox:checked');
        if (selectedCheckboxes.length === 0)
        {
            updateButton.textContent = "Update Information";
        }
        else 
        {
            updateButton.textContent = "Delete Product";
        }
        
    });

    toggleCheckboxes.forEach(checkbox =>
    {
        checkbox.addEventListener('change', () =>
        {
            const anyChecked = Array.from(toggleCheckboxes).some(checkbox => checkbox.checked);
            updateButton.textContent = anyChecked ? "Delete Products" : "Update Information";
        });
    })

    editForm.addEventListener('submit', async (event) =>
    {
        event.preventDefault();
        const selectedCheckboxes = document.querySelectorAll('.checkbox:checked');
        const selectedIDs = Array.from(selectedCheckboxes).map(checkbox => checkbox.value);
        if (selectedIDs.length === 0)
        {
            editForm.submit();
        }
        else
        {
            const response = await fetch('/delete_watches', {
                method: 'POST', headers: {'Content-Type': 'application/json'}, body: JSON.stringify({ watch_ids: selectedIDs})});
            if (response.ok) {
                this.location.reload();
            }
            else
            {
                console.error('Failed to delete products');
            }
        }
    });

    checkallbox.addEventListener('change', function() {
        toggleCheckboxes.forEach(checkbox => 
        {
            checkbox.checked = checkallbox.checked;
        });
    });
    
});

async function checkLoginStatus() {
    const response = await fetch('/check_session');
    const data = await response.json();
    const logoutButton = document.getElementById('logout');
    const loginButton = document.getElementById('login');

    if (data.session) {
        logoutButton.style.display = 'block';
        loginButton.style.display = 'none';
    } else {
        logoutButton.style.display = 'none';
        loginButton.style.display = 'block';
    }
}

window.onload = checkLoginStatus();
