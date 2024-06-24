import { useEffect } from "react";
import { Controller } from "react-hook-form";
import { deleteGlobalVariable } from "../../controllers/API";
import DeleteConfirmationModal from "../../modals/deleteConfirmationModal";
import useAlertStore from "../../stores/alertStore";
import { useGlobalVariablesStore } from "../../stores/globalVariablesStore/globalVariables";
import { InputGlobalComponentType } from "../../types/components";
import { cn } from "../../utils/utils";
import AddNewVariableButton from "../addNewVariableButtonComponent/addNewVariableButton";
import ForwardedIconComponent from "../genericIconComponent";
import InputComponent from "../inputComponent";
import { CommandItem } from "../ui/command";

export default function InputGlobalComponent({
  disabled,
  onChange,
  name,
  data,
  editNode = false,
}: InputGlobalComponentType): JSX.Element {
  const globalVariablesEntries = useGlobalVariablesStore(
    (state) => state.globalVariablesEntries,
  );

  const getVariableId = useGlobalVariablesStore((state) => state.getVariableId);
  const unavaliableFields = useGlobalVariablesStore(
    (state) => state.unavaliableFields,
  );
  const removeGlobalVariable = useGlobalVariablesStore(
    (state) => state.removeGlobalVariable,
  );
  const setErrorData = useAlertStore((state) => state.setErrorData);

  useEffect(() => {
    if (data && globalVariablesEntries && unavaliableFields)
      if (data.load_from_db && !globalVariablesEntries.includes(data.value)) {
        onChange("", false, true);
      } else if (
        !data.load_from_db &&
        (!data.value || data.value === "") &&
        unavaliableFields[data.display_name!] &&
        !disabled &&
        data.display_name
      ) {
        onChange(unavaliableFields[data.display_name!], true, true);
      }
  }, [globalVariablesEntries, unavaliableFields, data, disabled]);

  async function handleDelete(key: string) {
    const id = getVariableId(key);
    if (id !== undefined) {
      await deleteGlobalVariable(id)
        .then(() => {
          removeGlobalVariable(key);
          if (data?.value === key && data?.load_from_db) {
            onChange("", false);
          }
        })
        .catch(() => {
          setErrorData({
            title: "Error deleting variable",
            list: [cn("ID not found for variable: ", key)],
          });
        });
    } else {
      setErrorData({
        title: "Error deleting variable",
        list: [cn("ID not found for variable: ", key)],
      });
    }
  }
  return (
    <InputComponent
      id={"input-" + name}
      editNode={editNode}
      disabled={disabled}
      password={data.password ?? false}
      value={data.value ?? ""}
      options={globalVariablesEntries}
      optionsPlaceholder={"Global Variables"}
      optionsIcon="Globe"
      optionsButton={
        <AddNewVariableButton>
          <CommandItem value="doNotFilter-addNewVariable">
            <ForwardedIconComponent
              name="Plus"
              className={cn("mr-2 h-4 w-4 text-primary")}
              aria-hidden="true"
            />
            <span>Add New Variable</span>
          </CommandItem>
        </AddNewVariableButton>
      }
      optionButton={(option) => (
        <DeleteConfirmationModal
          onConfirm={(e) => {
            e.stopPropagation();
            e.preventDefault();
            handleDelete(option);
          }}
          description={'variable "' + option + '"'}
          asChild
        >
          <button
            onClick={(e) => {
              e.stopPropagation();
            }}
            className="pr-1"
          >
            <ForwardedIconComponent
              name="Trash2"
              className={cn(
                "h-4 w-4 text-primary opacity-0 hover:text-status-red group-hover:opacity-100",
              )}
              aria-hidden="true"
            />
          </button>
        </DeleteConfirmationModal>
      )}
      selectedOption={
        data?.load_from_db &&
        globalVariablesEntries &&
        globalVariablesEntries.includes(data?.value ?? "")
          ? data?.value
          : ""
      }
      setSelectedOption={(value) => {
        onChange(value, value !== "" ? true : false);
      }}
      onChange={(value, skipSnapshot) => {
        onChange(value, false, skipSnapshot);
      }}
    />
  );
}
