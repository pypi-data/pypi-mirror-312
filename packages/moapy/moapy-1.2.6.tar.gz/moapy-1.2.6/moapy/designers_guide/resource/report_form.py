from dataclasses import dataclass

@dataclass
class ReportForm:
    id: str = 'ID', # NOTE : Do not print to json
    standard: str = 'standard_number',
    reference: str = 'reference_section',
    title: str = 'title',
    description: str = 'description_for_content',
    figure_path: str = 'path_to_figure',
    descript_table: list = [],
    symbol: str = 'symbol_written_in_latex',
    formula: list = [],
    result: float = 0.0,
    result_table: list = [],
    ref_std: bool = False, # NOTE : Do not print to json
    unit: str = 'unit',
    notation: str = 'notation',
    decimal: int = 0,
    limits: dict = {},

    def to_dict(self):
        return {
            'standard': self.standard,
            'reference': self.reference if isinstance(self.reference, list) else [self.reference],
            'title': self.title,
            'description': self.description,
            'figure_path': self.figure_path,
            'descript_table': self.descript_table,
            'symbol': self.symbol,
            'formula': self.formula if isinstance(self.formula, list) else [self.formula],
            'result': str(self.result),
            'result_table': self.result_table if isinstance(self.result_table, list) else [self.result_table],
            # 'ref_std': self.ref_std,
            'unit': self.unit,
            'notation': self.notation,
            'decimal': self.decimal,
            'limits': self.limits if isinstance(self.limits, dict) else [self.limits],
        }
    
    def __repr__(self) -> str:
        full_formula = ""
        full_formula += f"{self.symbol}"
        for curr_formula in self.formula if self.formula else []:
            full_formula += " = " + f"{curr_formula}"
        full_formula += " = " + f"{self.result}" + f" {self.unit}"
                
        return (
            f"[{self.standard} {self.reference}] "
            f"{self.title}\n"
            f"{self.description}\n"
            f"{full_formula}"
        )