const BookList = {
    template: `
        <div>
            <input v-model="searchQuery" class="form-control mb-3" placeholder="Search books...">
            <table class="table">
                <thead>
                    <tr>
                        <th>Title</th>
                        <th>Author</th>
                        <th>Available</th>
                        <th>Actions</th>
                    </tr>
                </thead>
                <tbody>
                    <tr v-for="book in filteredBooks" :key="book.id">
                        <td>{{ book.title }}</td>
                        <td>{{ book.author }}</td>
                        <td>{{ book.quantity }}</td>
                        <td>
                            <button @click="editBook(book)" class="btn btn-sm btn-primary">Edit</button>
                            <button @click="deleteBook(book.id)" class="btn btn-sm btn-danger">Delete</button>
                        </td>
                    </tr>
                </tbody>
            </table>
        </div>
    `,
    data() {
        return {
            books: [],
            searchQuery: ''
        }
    },
    computed: {
        filteredBooks() {
            return this.books.filter(book =>
                book.title.toLowerCase().includes(this.searchQuery.toLowerCase()) ||
                book.author.toLowerCase().includes(this.searchQuery.toLowerCase())
            )
        }
    },
    methods: {
        async fetchBooks() {
            const response = await fetch('/api/books')
            this.books = await response.json()
        },
        // ... other methods
    },
    mounted() {
        this.fetchBooks()
    }
}
