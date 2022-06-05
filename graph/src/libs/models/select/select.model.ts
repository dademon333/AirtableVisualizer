import IControlOptions from "../../interfaces/control/control-options.interface";
import ISelect from "../../interfaces/control/select.interface";

export default class SelectModel<T> {
    private _items: Array<ISelect<T>>;
    private _selectedItem: ISelect<T> | null = null;
    private _onItemChange?: (item: ISelect<T>) => void;

    public options?: IControlOptions;

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
            return;
        }
        
        this._onItemChange?.call(this, this._selectedItem);
    }

    constructor(items: Array<ISelect<T>>, onItemChange?: (item: ISelect<T>) => void,  options?: IControlOptions) {
        this._onItemChange = onItemChange;
        this.options = options;
        if (items) {
            this._items = items;
            return;
        }

        console.warn('null or undefined items was provided');
        this._items = [];
    }
}