import ISelect from "../../interfaces/select/select.interface";

export default class SelectModel<T> {
    private _items: Array<ISelect<T>>;
    private _selectedItem: ISelect<T> | null = null;

    public get SelectedItem(): ISelect<T> | null {
        return this._selectedItem;
    }

    public get Items(): Array<ISelect<T>> {
        return this._items;
    }

    public set Items(items: Array<ISelect<T>>) {
        this._items = items;
    }

    public setSelectedItemById(id: string): void {
        this._selectedItem = this._items.find(item => item.id === id) || null;
        if (!this._selectedItem) {
            console.warn('unable to find select item with id ' + id);
        }
    }

    constructor(items: Array<ISelect<T>>) {
        if (items) {
            this._items = items;
            return;
        }

        console.warn('null or undefined items was provided');
        this._items = [];
    }
}