from graspnet_6dof.options.test_options import TestOptions
from graspnet_6dof.data import DataLoader
from graspnet_6dof.models import create_model
from graspnet_6dof.utils.writer import Writer


def run_test(epoch=-1, name=""):
    print('Running Test')
    opt = TestOptions().parse()
    opt.serial_batches = True  # no shuffle
    opt.name = name
    dataset = DataLoader(opt)
    model = create_model(opt)
    writer = Writer(opt)
    # test
    writer.reset_counter()

    for i, data in enumerate(dataset):
        model.set_input(data)
        ncorrect, nexamples = model.test()
        writer.update_counter(ncorrect, nexamples)
    writer.print_acc(epoch, writer.acc)
    return writer.acc


if __name__ == '__main__':
    run_test()
