class InitService:
    # Constants for data statuses
    SCRATCH = 0
    OUTDATED = 1
    UPTODATE = 2

    def inicializar(self):
        """
        Shared initialization logic for all service classes.
        """
        try:
            status = self.check_data_status()
            if status == self.SCRATCH:
                self.scratch_initialization()
            elif status == self.OUTDATED:
                self.update_data()
            elif status == self.UPTODATE:
                print("Data is up to date")
        except Exception as e:
            print(f"An error occurred: {e}")

    def check_data_status(self):
        """
        To be implemented by child classes to determine the data status.
        """
        raise NotImplementedError("Subclasses must implement checkDataStatus")

    def scratch_initialization(self):
        """
        To be implemented by child classes for scratch initialization.
        """
        raise NotImplementedError("Subclasses must implement scratchInitialization")

    def update_data(self):
        """
        To be implemented by child classes for data updates.
        """
        raise NotImplementedError("Subclasses must implement updateData")
