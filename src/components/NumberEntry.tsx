import Form from 'react-bootstrap/Form'; 
import '../App.css'

type Props = {
    value: number | string;
    onChange: (v: number) => void;
    placeholder?: string;
};
function NumberEntry({ value, onChange, placeholder }: Props) {
    return (
        <Form.Control className="col-12" size="sm" type="number"
        value={value}
        onChange={(e) => onChange(Number(e.target.value))}
                    placeholder={placeholder ?? "Value (e.g. 200)"}
      />
    
    )
}

export default NumberEntry;
