from pathlib import Path
class MonthlyEngine:
    def __init__(self, output_dir='reports', notify=None, completed=False):
        self.output_dir = Path(output_dir)
        self.notify = notify or (lambda record: record)
        self.completed = completed
    def run(self, target_date=None, force_send=False, reuse_context=False, format_test=False):
        if format_test:
            self.output_dir.mkdir(parents=True, exist_ok=True)
            path = self.output_dir / 'monthly_format_test.html'
            path.write_text('<html><body>Monthly</body></html>')
            return {'format_test': str(path)}
        record = {'target_date': target_date, 'reuse_context': reuse_context}
        if force_send or not self.completed:
            return self.notify(record)
        return {'skipped': True}
