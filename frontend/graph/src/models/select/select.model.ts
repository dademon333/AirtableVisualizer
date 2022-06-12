import { Observable, Subject } from "rxjs";
import IControlOptions from "../../interfaces/control/control-options.interface";
import ISelect from "../../interfaces/control/select.interface";
import Guid from "../../utils/guid";

export default class SelectModel<T> {
    private _items: Array<ISelect<T>>;
    private _selectedItem: ISelect<T> | null = null;
    private _onItemChange: Subject<ISelect<T>> = new Subject<ISelect<T>>();
    private _onDelete: Subject<void> = new Subject<void>();

    public options?: IControlOptions;

    /** Уникальный идентификатор контрола */
    public id: string;

    public get SelectedItem(): ISelect<T> | null {
        return this._selectedItem;
    }

    public get Items(): Array<ISelect<T>> {
        return this._items;
    }

    public set Items(items: Array<ISelect<T>>) {
        this._items = items;
    }

    public get OnDelete(): Observable<void> {
        return this._onDelete.asObservable();
    }

    public get OnItemChange(): Observable<ISelect<T>> {
        return this._onItemChange.asObservable();
    }

    public emitOnDelete(): void {
        this._onDelete.next();
    }
 
    public setSelectedItemById(id: string): void {
        this._selectedItem = this._items.find(item => item.id === id) || null;
        if (!this._selectedItem) {
            console.warn('unable to find select item with id ' + id);
            return;
        }
        
        this._onItemChange?.next(this.SelectedItem!);
    }

    constructor(items: Array<ISelect<T>>, options?: IControlOptions, defaultValue?: ISelect<T>) {
        this.options = options;
        this.id = Guid.newGuid();


        if (items) {
            this._items = items;
            if (defaultValue) {
                this.setSelectedItemById(defaultValue.id);
            }
            return;
        }

        console.warn('null or undefined items was provided');
        this._items = [];
        if (defaultValue) {
            this.setSelectedItemById(defaultValue.id);
        }
    }
}